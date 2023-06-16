import os
from io import BytesIO

import discord
import requests
from discord.ext import commands
from PIL import Image


class SpecialEventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="деньлогова2022")
    async def logowo_day(self, ctx):
        frame = Image.open(os.path.join('app', 'assets', 'frame.png'))
        if not ctx.interaction:
            await ctx.send("ща будет жди")
        await ctx.defer()
        with requests.get(ctx.author.avatar.url, timeout=10) as req:
            img_data = req.content
            ava = Image.open(BytesIO(img_data))
        ava = ava.resize((2000, 2000))
        ava.paste(frame, (0, 0), frame)
        with BytesIO() as image_binary:
            ava.save(image_binary, "PNG")
            image_binary.seek(0)
            await ctx.send(
                file=discord.File(fp=image_binary, filename="result.png")
            )

    @commands.hybrid_command(name="деньлогова2023")
    async def logovo_day(self, ctx):
        frame2 = Image.open(os.path.join('app', 'assets', 'frame2.png'))
        if not ctx.interaction:
            await ctx.send("ща будет жди")
        await ctx.defer()
        with requests.get(ctx.author.avatar.url, timeout=10) as req:
            img_data = req.content
            ava = Image.open(BytesIO(img_data))
        ava = ava.resize((1024, 1024))
        ava.paste(frame2, (0, 0), frame2)
        with BytesIO() as image_binary:
            ava.save(image_binary, "PNG")
            image_binary.seek(0)
            await ctx.send(
                file=discord.File(fp=image_binary, filename="result.png")
            )
