from app.config import cmd_manager
from app.bot.commands_exceptions import *
import requests
from io import BytesIO
from PIL import Image
import discord
import os


@cmd_manager.command("деньлогова2022")
async def logowo_day(msg):
    frame = Image.open(os.path.join('assets', 'frame.png'))
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

@cmd_manager.command("деньлогова2023")
async def logovo_day(msg):
    frame2 = Image.open(os.path.join('assets', 'frame2.png'))
    await msg.channel.send("ща будет жди")
    with requests.get(msg.author.avatar.url) as r:
        img_data = r.content
        ava = Image.open(BytesIO(img_data))
    ava = ava.resize((1024, 1024))
    ava.paste(frame2, (0, 0), frame2)
    with BytesIO() as image_binary:
        ava.save(image_binary, "PNG")
        image_binary.seek(0)
        await msg.channel.send(
            file=discord.File(fp=image_binary, filename="result.png")
        )