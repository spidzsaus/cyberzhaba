import discord
from discord.ext import commands

from app.db.models import SqlUser
from app.helper_tools import basic_embed
from app.entities.users import User
from app.checks import is_bot_moderator
from app.db import database


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="блеклист", fallback="участники",
        description="посмотреть чёрный список Криптожабы."
    )
    @is_bot_moderator()
    async def blacklist(self, ctx):
        db_sess = database.session()
        users = db_sess.query(SqlUser).filter(SqlUser.blacklist == True)
        embed = basic_embed(
            title="Чёрный список Криптожабы.", text="Вот они, сверху вниз:"
        )
        for i, user in enumerate(users):
            user = await self.bot.fetch_user(user.discord_id)
            embed.add_field(name=str(i + 1) + ". " + user.name, value="_ _")
        await ctx.send(embed=embed)

    @blacklist.command(
        name="добавить",
        description="добавить кого-то в чёрный список."
    )
    @discord.app_commands.rename(discord_user="цель")
    @discord.app_commands.describe(discord_user="кого добавить в список")
    @is_bot_moderator()
    async def blacklist_add(self, ctx, discord_user: discord.User):
        user = User(discord_user.id)
        user.add_to_blacklist()
        embed = basic_embed(
            title=discord_user.name + " добавлен в чёрный список.",
            text="Смейтесь его! Гоняйте над ним!",
        )
        if discord_user.avatar:
            embed.set_thumbnail(url=discord_user.display_avatar.url)
        await ctx.send(embed=embed)

    @blacklist.command(
        name="убрать",
        description="убрать кого-то из чёрного списка."
    )
    @discord.app_commands.rename(discord_user="цель")
    @discord.app_commands.describe(discord_user="кого убрать из списка")
    @is_bot_moderator()
    async def blacklist_remove(self, ctx, discord_user: discord.User):
        user = User(discord_user.id)
        user.remove_from_blacklist()
        embed = basic_embed(
            title=discord_user.name + " вычтен из чёрного списка.",
            text="на этот раз прощаем.",
        )
        if discord_user.avatar:
            embed.set_thumbnail(url=discord_user.display_avatar.url)
        await ctx.send(embed=embed)
