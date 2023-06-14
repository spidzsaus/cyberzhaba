from config import cmd_manager
from bot.commands_exceptions import *
import asyncio
import discord
from helper_tools import basic_embed
import os
from barrellorgans import BarellOrgan
import datetime as dt


@cmd_manager.command("шарманка")
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