from datetime import datetime, timedelta

import discord
from discord.ext import commands

from app.entities.users import User
from app.entities.memberships import Membership
from app.helper_tools import basic_embed
from app.db.models import SqlMembership
from app.db import database


class LastActivityCog(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="активность",
        description="список активных логовцев."
    )
    @discord.app_commands.rename(
        user="пользователь", admin_mode="судебный_режим"
    )
    @discord.app_commands.describe(
        user="чью активность посмотреть? (оставить пустым для списка)",
        admin_mode="отладочная информация для судей"
    )
    async def activity_info(
        self, ctx, user: discord.User | None, admin_mode: bool = False
    ):
        ent_author = User(ctx.author.id)

        level = 0
        if admin_mode and ent_author.sql().mod:
            level = 2
        elif admin_mode and ctx.author.guild_permissions.manage_guild:
            level = 1
        elif admin_mode:
            await ctx.send(
                embed=basic_embed(
                    ":x: заборонено",
                    "ты не судья!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
        ephemeral = level > 0 and (ctx.guild is not None)

        if user is None:
            if ctx.guild is None:
                await ctx.send(
                    embed=basic_embed(
                        ":x: невозможно посмотреть список",
                        "лс - не сервер, здесь только ты и бот!",
                        color=discord.Color.red()
                    )
                )
                return
            info = ""
            three_days_ago = datetime.now() - timedelta(days=3)
            db_sess = database.session()
            memberships = (
                db_sess.query(SqlMembership)
                .filter(
                    SqlMembership.karma >= 1,
                    SqlMembership.guild == ctx.guild.id,
                    SqlMembership.last_activity > three_days_ago
                ).order_by(SqlMembership.last_activity.desc())
            )
            for i, membership in enumerate(memberships):
                dt = discord.utils.format_dt(
                    membership.last_activity, "R"
                )
                info += f"{i}. <@!{membership.user}> ({dt})\n"
            info += "\nотображаются последние активщики за три дня"
            await ctx.send(
                embed=basic_embed(
                    "вот они, активные логовцы, сверху вниз:", info
                ),
                ephemeral=ephemeral
            )
        else:
            ent_user = User(user.id)
            db_user = ent_user.sql()
            if ctx.guild is not None:
                ent_membership = Membership(user.id, ctx.guild.id)
                db_membership = ent_membership.sql()
            else:
                ent_membership = None
                db_membership = None

            if db_user.last_activity is None:
                await ctx.send(
                    embed=basic_embed(
                        ":x: дата недоступна",
                        "пользователь ничего не делал после введения этой фичи",
                        color=discord.Color.red()
                    ),
                    ephemeral=True
                )
                return

            info = ""
            if db_membership is not None \
               and db_membership.last_activity is not None:
                dt = discord.utils.format_dt(db_membership.last_activity)
                info += f"**Активность на сервере:** {dt}\n"
                if level >= 1:
                    info += f"**Тип активности:** \
{db_membership.last_activity_type}\n"

            if level >= 2:
                dt = discord.utils.format_dt(db_user.last_activity)
                info += f"**Общая активность:** {dt}\n"
                info += f"**Тип активности:** {db_user.last_activity_type}"

            embed = basic_embed(f"{user.name}", text=info)
            if user.avatar:
                embed.set_thumbnail(url=user.avatar.url)

            await ctx.send(embed=embed, ephemeral=ephemeral)

    def __mark_activity(
        self, uid: int, gid: int | None = None,
        activity_type: str = ""
    ):
        if type(uid) != int:
            return
        user = User(uid)
        user.mark_activity(activity_type)
        if type(gid) == int:
            membership = Membership(uid, gid)
            membership.mark_activity(activity_type)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is not None:
            self.__mark_activity(
                message.author.id, message.guild.id,
                f"message in <#{message.channel.id}>"
            )
        else:
            self.__mark_activity(
                message.author.id,
                activity_type=f"bot direct message"
            )

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        # try:
        #     channel = await self.bot.fetch_channel(payload.channel_id)
        #     message = await channel.fetch_message(payload.message_id)
        # except Exception:
        #     pass
        # self.__mark_activity(
        #     message.author.id, channel.guild.id,
        #     f"message edited in <#{payload.channel_id}>"
        # )
        pass

    @commands.Cog.listener()
    async def on_raw_typing(self, payload: discord.RawTypingEvent):
        self.__mark_activity(
            payload.user_id, payload.guild_id,
            f"typing in <#{payload.channel_id}>"
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        self.__mark_activity(
            payload.user_id, payload.guild_id,
            f"reaction in <#{payload.channel_id}>"
        )

    @commands.Cog.listener()
    async def on_raw_poll_vote_add(self, payload: discord.RawPollVoteActionEvent):
        self.__mark_activity(
            payload.user_id, payload.guild_id,
            f"poll vote in <#{payload.channel_id}>"
        )

    @commands.Cog.listener()
    async def on_raw_poll_vote_remove(self, payload: discord.RawPollVoteActionEvent):
        self.__mark_activity(
            payload.user_id, payload.guild_id,
            f"poll vote revoked in <#{payload.channel_id}>"
        )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, *args):
        self.__mark_activity(
            member.id, member.guild.id,
            f"voice state update in server {member.guild.name}"
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        self.__mark_activity(
            member.id, member.guild.id,
            f"joined server {member.guild.name}"
        )

    @commands.Cog.listener()
    async def on_user_update(self, _, after: discord.User):
        self.__mark_activity(
            after.id,
            activity_type="profile update"
        )

    @commands.Cog.listener()
    async def on_presence_update(self, _, after: discord.Member):
        self.__mark_activity(
            after.id,
            activity_type="presence update"
        )
