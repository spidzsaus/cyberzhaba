import math

from sqlalchemy import func
import discord
from discord.ext import commands

from app.db.models import SqlReactionRole
from app.helper_tools import basic_embed, AnyEmojiConverter
from app.entities.reactionroles import ReactionRole
from app.db import database
from app.checks import is_bot_moderator
from app.exceptions import NotFound


class ReactionRolesCog(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = await channel.guild.fetch_member(payload.user_id)
        raw_emoji = payload.emoji
        if raw_emoji.id is not None:
            emoji = await channel.guild.fetch_emoji(raw_emoji.id)
        else:
            emoji = str(raw_emoji)

        rr = ReactionRole.search(message=message, reaction=emoji)
        if rr:
            await message.remove_reaction(emoji, member)
            role = await rr.get_role(self.bot)
            if role is None:
                return
            if member.get_role(rr.role_id) is None:
                await member.add_roles(role)
                try:
                    await member.send(
                        embed=basic_embed(None, f"✅ Выдана роль `{role.name}`")
                    )
                except Exception as err:
                    pass
            else:
                await member.remove_roles(role)
                try:
                    await member.send(
                        embed=basic_embed(None, f"✅ Снята роль `{role.name}`")
                    )
                except Exception:
                    pass

    @commands.hybrid_group(
        name="галочки", fallback="список",
        description="посмотреть полный список галочных сообщений."
    )
    @discord.app_commands.rename(page="номер_страницы")
    @discord.app_commands.describe(page='какую страницу открыть')
    @is_bot_moderator()
    async def reactionrole(self, ctx, page: int = 1):
        db_sess = database.session()
        total_count = db_sess.query(func.count(SqlReactionRole.id)).scalar()
        maxpage = math.ceil(total_count / 10)
        page = max(1, min(maxpage, page))
        reactionroles = (
            db_sess.query(SqlReactionRole)
            .offset((page - 1) * 10)
            .limit(10)
            .all()
        )

        text = ""
        for rr in reactionroles:
            rr_entity = ReactionRole(rr)
            try:
                emoji_text = str(await rr_entity.get_emoji(self.bot))
            except discord.errors.Forbidden:
                text += f"⚠️ ID:{rr_entity.id} - <@&{rr.role_id}> \
в <#{rr.channel_id}>, НЕТ ДОСТУПА\n"
                continue
            error_emoji = ""
            message = await rr_entity.get_message(self.bot)
            message_text = message.to_reference().jump_url if message else 'СООБЩЕНИЕ УДАЛЕНО'
            if message_text == 'СООБЩЕНИЕ УДАЛЕНО':
                error_emoji = "⚠️ "
            role = await rr_entity.get_role(self.bot)
            role_text = role.mention if role else 'РОЛЬ УДАЛЕНА'
            if not role:
                error_emoji = "⚠️ "
            text += f"{error_emoji}ID:{rr_entity.id} - {emoji_text} {message_text} {role_text}"
            text += '\n'
        embed = basic_embed(
            title=f"Список галоcheck (Страница {page}/{maxpage})",
            text=text,
        )

        await ctx.send(embed=embed)

    @reactionrole.command(
        name='создать',
        description='создать галочку'
    )
    @discord.app_commands.rename(
        message='сообщение',
        role='роль',
        emoji='эмодзи'
    )
    @discord.app_commands.describe(
        message='ссылка на сообщение, на котором будет создана галочка',
        role='роль, присваемая по нажатию на галочку',
        emoji='эмодзи, которое будет галочкой галочного сообщения'
    )
    @is_bot_moderator()
    async def reactionrole_create(
        self,
        ctx,
        message: discord.Message,
        role: discord.Role,
        emoji: AnyEmojiConverter
    ):
        await message.add_reaction(emoji)
        ReactionRole.create(message, emoji, role)
        await ctx.send(embed=basic_embed(
            'Готово!',
            'Галочка создана'
        ))

    @reactionrole.command(
        name='удалить',
        description='удалить галочку'
    )
    @discord.app_commands.rename(
        rrid='id'
    )
    @is_bot_moderator()
    async def reactionrole_delete(self, ctx, rrid: int):
        db_sess = database.session()
        reaction_role = db_sess.query(SqlReactionRole).filter(
            SqlReactionRole.id == rrid
        )
        if not reaction_role:
            raise NotFound(f'Reactionrole with id {rrid} does not exist')
        rr_entity = ReactionRole(reaction_role.first())
        message = await rr_entity.get_message(self.bot)
        emoji = await rr_entity.get_emoji(self.bot)
        if message and emoji:
            await message.remove_reaction(
                emoji=emoji,
                member=self.bot.user
            )
        reaction_role.delete()
        db_sess.commit()
        await ctx.send(embed=basic_embed(
            'Готово!',
            'Галочка удалена'
        ))
