from app.config import cmd_manager
from app.bot.commands_exceptions import *
from app.db import db_session
from app.db.usermodel import SqlUser
import math
import discord
from app.helper_tools import basic_embed
from app.entities.users import User


@cmd_manager.command("карма")
async def view_karma(msg):
    args = msg.content.split()
    if len(args) == 1:
        user = User(msg.author.id)
    else:
        user = User.from_string(args[1])
        if not user:
            embed = basic_embed(":x: Ээээ....", "кто?")
            embed.color = discord.Color.red()
            await msg.channel.send(embed=embed)
            return
    duser = await user.DISCORD()
    embed = basic_embed(
        "Профиль " + duser.name, "Постовая карма: " + str(user.karma)
    )
    if duser.avatar:
        embed.set_thumbnail(url=duser.avatar.url)
    await msg.channel.send(embed=embed)


@cmd_manager.command("лидеры")
async def leaderboard(msg):
    args = msg.content.split()
    if len(args) == 1:
        page = 1
    else:
        try:
            page = int(args[1])
        except ValueError:
            page = 1

    db_sess = db_session.create_session()
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

    await msg.channel.send(embed=embed)
