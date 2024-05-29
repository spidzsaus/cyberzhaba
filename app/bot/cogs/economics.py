import math

import discord
from discord.ext import commands

from app.db.models import SqlMembership
from app.helper_tools import basic_embed
from app.entities.users import User
from app.entities.guilds import Guild
from app.entities.memberships import Membership
from app.checks import is_bot_moderator
from app.db import database


class EconomicsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(
        name="карма-каналы",
        description="список каналов и категорий, в которых засчитывается карма"
    )
    @commands.guild_only()
    async def karma_channel_list(self, ctx):
        config = Guild(ctx.guild.id).config
        channel_whitelist = config.get('karma.channel_whitelist', [])
        channel_whitelist_keywords = config.get(
            'karma.channel_whitelist_keywords', []
        )
        category_whitelist = config.get('karma.category_whitelist', [])

        result = ""
        for category_id in category_whitelist:
            category = ctx.guild.get_channel(category_id)
            if category:
                result += f'* Вся категория **{category.name}**\n'

        for channel in ctx.guild.channels:
            if channel.category and channel.category.id \
                in category_whitelist:
                continue
            channel_whitelisted = channel.id in channel_whitelist
            keyword_whitelisted = True in [
                word in channel.name for word in
                channel_whitelist_keywords
            ]
            if channel_whitelisted or keyword_whitelisted:
                result += f'* <#{channel.id}>\n'

        embed = basic_embed(
            title="Все каналы с работающей кармой",
            text=result
        )

        await ctx.send(embed=embed)


    @commands.hybrid_command(
        name="карма",
        description="посмотреть свою или чью-то карму."
    )
    @discord.app_commands.rename(member="цель")
    @discord.app_commands.describe(member='чью карму посмотреть')
    @commands.guild_only()
    async def view_karma(self, ctx, member: discord.Member | None):
        if not member:
            member = ctx.author

        membership = Membership(member.id, ctx.guild.id)

        embed = basic_embed(
            "Профиль " + member.name, "Постовая карма: " + str(membership.karma)
        )
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        await ctx.send(embed=embed)


    @commands.hybrid_command(
        name="лидеры",
        description="топ кармов."
    )
    @discord.app_commands.rename(page="номер_страницы")
    @discord.app_commands.describe(page='какую страницу открыть')
    @commands.guild_only()
    async def leaderboard(self, ctx, page: int = 1):
        db_sess = database.session()
        memberships = (
            db_sess.query(SqlMembership)
            .filter(SqlMembership.karma != 0)
            .order_by(SqlMembership.karma.desc())
        )

        maxpage = math.ceil(memberships.count() / 10)
        page = max(1, min(maxpage, page))
        text = ""
        for i, membership in enumerate(memberships[(page - 1) * 10 : page * 10]):
            text += (
                "**"
                + str((page - 1) * 10 + i + 1)
                + ".** `["
                + str(membership.karma)
                + "]` <@!"
                + str(membership.user.discord_id)
                + ">\n"
            )
        embed = basic_embed(
            title="Топ кармов (Страница " + str(page) + "/" + str(maxpage) + ")",
            text=text,
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="переместитькарму",
        description="переместить карму с участника на участника."
    )
    @discord.app_commands.rename(
        source="источник", target="цель", confirm_code="код"
    )
    @discord.app_commands.describe(
        source="кто ПОТЕРЯЕТ карму", target="кто ПОЛУЧИТ карму",
        confirm_code="код подтверждения - введите команду без него, чтобы получить"
    )
    @is_bot_moderator()
    @commands.guild_only()
    async def move_karma(
        self, ctx, source: discord.Member, target: discord.Member,
        confirm_code: str | None
    ):
        real_confirm_code = str(source.id)[-4:-1] + str(target.id)[-4:-1]
        if not confirm_code:
            await ctx.send(
                f"Переместить карму с участника `{source.name}` на `{target.name}`\
...вы уверены? **ЭТО НЕОБРАТИМАЯ ОПЕРАЦИЯ.**\n\n\
Перезапустите команду с кодом `{real_confirm_code}`, если да."
            )
            return
        if confirm_code != real_confirm_code:
            await ctx.send(f"Неправильный код. Введите код `{real_confirm_code}`.")
            return

        db_sess = database.session()
        source_db = db_sess.query(SqlMembership).filter(
            SqlMembership.user == source.id,
            SqlMembership.guild == ctx.guild.id
        ).first()
        target_db = db_sess.query(SqlMembership).filter(
            SqlMembership.user == target.id,
            SqlMembership.guild == ctx.guild.id
        ).first()

        target_db.karma += source_db.karma
        source_db.karma = 0

        db_sess.commit()

        await ctx.send(f"Дело сделано... \
У {target.mention} теперь **{target_db.karma}** кармы.")

    async def reaction_event(self, payload, meaning=1):
        channel = await self.bot.fetch_channel(payload.channel_id)
        guild = channel.guild
        msg = await channel.fetch_message(payload.message_id)
        if msg.webhook_id:
            return
        user = await self.bot.fetch_user(payload.user_id)
        if user.id == msg.author.id or user.bot or msg.author.bot:
            return

        config = Guild(guild.id).config
        channel_whitelist = config.get('karma.channel_whitelist', [])
        channel_whitelist_keywords = config.get(
            'karma.channel_whitelist_keywords', []
        )
        category_whitelist = config.get('karma.category_whitelist', [])
        praise = config.get('karma.emojis', [])

        category_whitelisted = channel.category and (
            channel.category_id in category_whitelist
        )
        channel_whitelisted = payload.channel_id in channel_whitelist
        keyword_whitelisted = True in [
            word in channel.name for word in channel_whitelist_keywords
        ]

        if not (category_whitelisted or channel_whitelisted or keyword_whitelisted):
            return
        if User(payload.user_id).is_blacklisted() or User(msg.author.id).is_blacklisted():
            return

        if payload.emoji.id in praise:
            membership = Membership(msg.author.id, guild.id)
            membership.add_karma(config.get("karma.coeff", 1) * meaning)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.reaction_event(payload, 1)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.reaction_event(payload, -1)
