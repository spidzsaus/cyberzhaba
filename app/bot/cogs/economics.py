import math

import discord
from discord.ext import commands

from app.db.usermodel import SqlUser
from app.helper_tools import basic_embed
from app.entities.users import User
from app.config import logovo_config
from app.db import database


class EconomicsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="карма",
        description="посмотреть свою или чью-то карму."
    )
    @discord.app_commands.rename(duser="цель")
    @discord.app_commands.describe(duser='чью карму посмотреть')
    async def view_karma(self, ctx, duser: discord.User | None):
        if not duser:
            duser = ctx.author
        user = User(duser.id)
        embed = basic_embed(
            "Профиль " + duser.name, "Постовая карма: " + str(user.karma)
        )
        if duser.avatar:
            embed.set_thumbnail(url=duser.avatar.url)
        await ctx.send(embed=embed)


    @commands.hybrid_command(
        name="лидеры",
        description="топ кармов."
    )
    @discord.app_commands.rename(page="номер_страницы")
    @discord.app_commands.describe(page='какую страницу открыть')
    async def leaderboard(self, ctx, page: int = 1):
        db_sess = database.session()
        users = (
            db_sess.query(SqlUser)
            .filter(SqlUser.karma != 0)
            .order_by(SqlUser.karma.desc())
        )
        maxpage = math.ceil(users.count() / 10)
        page = max(1, min(maxpage, page))
        text = ""
        for i, user in enumerate(users[(page - 1) * 10 : page * 10]):
            text += (
                "**"
                + str((page - 1) * 10 + i + 1)
                + ".** `["
                + str(user.karma)
                + "]` <@!"
                + str(user.discord_id)
                + ">\n"
            )
        embed = basic_embed(
            title="Топ кармов (Страница " + str(page) + "/" + str(maxpage) + ")",
            text=text,
        )

        await ctx.send(embed=embed)

    async def reaction_event(self, payload, meaning=1):
        channel = await self.bot.fetch_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        if msg.webhook_id:
            return
        user = await self.bot.fetch_user(payload.user_id)
        if user.id == msg.author.id or user.bot or msg.author.bot:
            return

        category_whitelisted = channel.category and (
            channel.category_id in logovo_config['category_whitelist']
        )
        channel_whitelisted = payload.channel_id in logovo_config['channel_whitelist']
        keyword_whitelisted = True in [
            word in channel.name for word in logovo_config['channel_whitelist_keywords']
        ]

        if not (category_whitelisted or channel_whitelisted or keyword_whitelisted):
            return
        if User(payload.user_id).is_blacklisted() or User(msg.author.id).is_blacklisted():
            return
       # if days_delta(msg) >= CONFIG['message_expiration_date']:
       #     return
        if payload.emoji.id in logovo_config['praise']:
            user = User(msg.author.id)
            user.add_karma(logovo_config['coeff'] * meaning)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.reaction_event(payload, 1)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.reaction_event(payload, -1)
