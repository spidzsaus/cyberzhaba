from hub import command, AccessDeniedError, __Client__
from db import db_session
from db.usermodel import SqlUser, SqlBarrellOrgan
import math
import requests
from io import BytesIO
from PIL import Image
import asyncio
import discord
from helper_tools import basic_embed
import os

from users import User
from barrellorgans import BarellOrgan

import datetime as dt


def days_delta(msg):
    now = dt.datetime.today()
    delta = now - msg.created_at
    return delta.days


frame = Image.open("frame.png")
frame2 = Image.open("frame2.png")

@command("карма")
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


@command("шарманка")
async def barrel_organ(msg):
    user = msg.author
    if dt.datetime.now() < dt.datetime(2023, 1, 1, 8, 30, 0, 0):
        embed = basic_embed(
            title="Рано...",
            text="christmas! just a week away! oh wow! christmas is in a week!",
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url=user.avatar.url)
        await msg.channel.send(embed=embed)
        return

    barrellorgan = BarellOrgan.__new__(BarellOrgan, user.id)

    if not barrellorgan:
        embed = basic_embed(
            title="Увы, у тебя нет шарманки",
            text="Это грустно :( Но возможно, она у тебя скоро появится....",
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url=user.avatar.url)
        await msg.channel.send(embed=embed)
        return

    embed, image = barrellorgan.preview()
    embed.set_thumbnail(url=user.avatar.url)
    await msg.channel.send(embed=embed, file=image)

    voice_channel = user.voice
    if voice_channel:
        voice_channel = voice_channel.channel
    if voice_channel != None:
        embed = basic_embed(
            user.name + " запустил свою шарманку",
            "Все присутствующие в " + voice_channel.name + " ошеломлены..",
        )
        embed.set_thumbnail(url=user.avatar.url)
        await msg.channel.send(embed=embed)

        voice_client = msg.guild.voice_client

        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()

        await voice_channel.connect()

        voice_client = msg.guild.voice_client

        voice_client.play(
            discord.FFmpegPCMAudio(
                source=os.path.join(barrellorgan.path, "melody.mp3"),
                executable="FFMPEG/ffmpeg.exe",
            )
        )

        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()


@command("деньлогова2022")
async def logowo_day(msg):
    await msg.channel.send("ща будет жди")
    with requests.get(msg.author.avatar.url) as r:
        img_data = r.content
        ava = Image.open(BytesIO(img_data))
    ava = ava.resize((2000, 2000))
    ava.paste(frame, (0, 0), frame)
    with BytesIO() as image_binary:
        ava.save(image_binary, "PNG")
        image_binary.seek(0)
        await msg.channel.send(
            file=discord.File(fp=image_binary, filename="result.png")
        )

@command("деньлогова2023")
async def logovo_day(msg):
    await msg.channel.send("ща будет жди")
    with requests.get(msg.author.avatar.url) as r:
        img_data = r.content
        ava = Image.open(BytesIO(img_data))
    ava = ava.resize((2000, 2000))
    ava.paste(frame2, (0, 0), frame2)
    with BytesIO() as image_binary:
        ava.save(image_binary, "PNG")
        image_binary.seek(0)
        await msg.channel.send(
            file=discord.File(fp=image_binary, filename="result.png")
        )


@command("хелп")
async def help(msg):
    embed = basic_embed(
        "Справка",
        "**кж!карма** - посмотреть свой профиль.\n"
        "**кж!карма {пользователь}** - посмотреть чужой профиль.\n"
        "**кж!лидеры {страница}** - посмотреть список лидеров по карме.",
    )
    await msg.channel.send(embed=embed)


@command("лидеры")
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


@command("блеклист")
async def blacklist(msg):
    if not User(msg.author.id).SQL().mod:
        raise AccessDeniedError
    args = msg.content.split()
    if len(args) == 1:
        db_sess = db_session.create_session()
        users = db_sess.query(SqlUser).filter(SqlUser.blacklist == True)
        embed = basic_embed(
            title="Чёрный список Криптожабы.", text="Вот они, сверху вниз:"
        )
        for i, user in enumerate(users):
            u = await User(user.discord_id).DISCORD()
            embed.add_field(name=str(i + 1) + ". " + u.name, value="_ _")
        await msg.channel.send(embed=embed)
    elif args[1] == "добавить":
        user = User(int(msg.content.split()[2]))
        user.add_to_blacklist()
        d = await user.DISCORD()
        embed = basic_embed(
            title=d.name + " добавлен в чёрный список.",
            text="Смейтесь его! Гоняйте над ним!",
        )
        if d.avatar:
            embed.set_thumbnail(url=d.avatar_url)
        await msg.channel.send(embed=embed)
    elif args[1] == "убрать":
        user = User(int(msg.content.split()[2]))
        user.remove_from_blacklist()
        d = await user.DISCORD()
        embed = basic_embed(
            title=d.name + " вычтен из чёрного списка.",
            text="на этот раз прощаем.",
        )
        if d.avatar:
            embed.set_thumbnail(url=d.avatar_url)
        await msg.channel.send(embed=embed)
