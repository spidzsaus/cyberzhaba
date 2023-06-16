import shutil
import discord


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
