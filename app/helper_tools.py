import shutil
import emoji
import discord
from discord.ext import commands


def basic_embed(title, text, *fields, color=discord.Color.green()):
    emb = discord.Embed(color=color,
                        title=title,
                        description=text)
    for name, value in fields:
        emb.add_field(name=name, value=value)
    return emb


def broken_cyberzhaba(description):
    return basic_embed(
        title=":x: кто-то сломал криптожабу. они за это заплатят.",
        text=description,
        color=discord.Color.red(),
    )


def find_ffmpeg():
    executable = shutil.which('ffmpeg')
    if not executable:
        executable = shutil.which('FFMPEG/ffmpeg.exe')
    if not executable:
        executable = shutil.which('FFMPEG/ffmpeg')
    if not executable:
        executable = shutil.which('FFMPEG/ffmpeg.x86_64')
    return executable


def none_on_catch(exception: Exception):
    def wrapper(func):
        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception:
                return None
        return new_func
    return wrapper


def async_none_on_catch(exception: Exception):
    def wrapper(func):
        async def new_func(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exception:
                return None
        return new_func
    return wrapper


def assert_unicode_emoji(val):
    '''Checks if val is a unicode emoji'''
    val = str(val)
    if not emoji.is_emoji(val):
        raise TypeError(f'{val} is not a single emoji')
    return val


class AnyEmojiConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return await commands.EmojiConverter().convert(ctx, argument)
        except commands.EmojiNotFound:
            return assert_unicode_emoji(argument)
