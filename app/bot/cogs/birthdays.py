import datetime as dt

import discord
from discord.ext import commands, tasks
import dateparser

from app.entities.guilds import Guild
from app.entities.users import User
from app.db.models import SqlUser, SqlMembership, SqlGuild
from app.db import database
from app.helper_tools import basic_embed
from app.checks import is_bot_moderator
from app import config


class BirthdaysCog(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.birthday_alert_loop.start()

    @tasks.loop(hour=0, minute=0, tzinfo=config.TIMEZONE)
    async def birthday_alert_loop(self):
        db_sess = database.session()
        today = dt.date.today()

        for guild in self.bot.guilds:
            guild_config = Guild(guild.id).config
            alert_channel = guild.get_channel_or_thread(
                guild_config.get("alert_channel")
            )
            if alert_channel is None:
                continue

            memberships = db_sess.query(SqlMembership, SqlUser).filter(
                SqlMembership.user == SqlUser.discord_id,
                SqlMembership.guild == guild.id,
                SqlUser.birthday != None
            ).all()

            birthdays = []
            any_reminder = False
            for membership, user in memberships:
                birthday = user.birthday.replace(
                    year=dt.datetime.now().year
                )
                if today > birthday:
                    birthday = birthday.replace(
                        year=birthday.year + 1
                    )

                days_till = (birthday - dt.date.today()).days

                this_reminder = days_till in (0, 1, 3, 7, 14)
                any_reminder = any_reminder or this_reminder

                if 0 <= days_till <= 14:
                    birthdays.append(
                        (birthday, user.discord_id, this_reminder)
                    )

            if not any_reminder:
                continue

            text = ""
            for date, discord_id, this_reminder in sorted(
                birthdays, key=lambda x: x[0]
            ):
                datetime = dt.datetime.combine(
                    date, dt.time(tzinfo=config.TIMEZONE)
                )
                date_text = date.strftime("%d.%m.%y")
                icon = "🔔 " if this_reminder else ""
                text += f"* {icon}{date_text} \
{discord.utils.format_dt(datetime, style='R')} <@!{discord_id}>\n"

            text = text.rstrip("\n") + "\n\n⚠️ отсчитывается время до полуночи МСК"

            await alert_channel.send(
                embed=basic_embed("🍰 Предстоящие дни рождения", text)
            )

    @commands.hybrid_command(
        "деньрождения",
        description="посмотреть или установить чей-то день рождения."
    )
    @discord.app_commands.rename(user="юзер", birthday="день_рождения")
    @discord.app_commands.describe(
        user="чей день рождения",
        birthday="2006-01-13, 13 января 2006 и т.д..."
    )
    @is_bot_moderator()
    async def birthday_command(
        self, ctx, user: discord.User, *, birthday: str | None
    ):
        db_user = User(user.id)
        if not birthday or birthday.strip() == "":
            await ctx.send(db_user.sql().birthday or "-")
            return
        date = dateparser.parse(
            birthday, settings={
                "REQUIRE_PARTS": ["day", "month"],
                "PREFER_DATES_FROM": "past"
            }
        )
        if not date:
            await ctx.send("непонятная дата")
            return
        date = date.date() # get rid of the time part
        if date.year >= date.today().year:
            date = date.replace(year=1604)
        db_user.set_birthday(date)
        await ctx.send(f"установлено {date}")
