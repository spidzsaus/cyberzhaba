from discord.ext import commands

from app.entities.users import User
from app.helper_tools import find_ffmpeg


class BotModeratorsOnlyError(commands.CheckFailure):
    pass


class MissingFFMPEGError(commands.CheckFailure):
    pass


def is_bot_moderator():
    async def predicate(ctx):
        if ctx.author.id == ctx.bot.application.owner.id:
            return True
        if not User(ctx.author.id).sql().mod:
            raise BotModeratorsOnlyError()
        return True
    return commands.check(predicate)


def requires_ffmpeg():
    async def predicate(_):
        if not find_ffmpeg():
            raise MissingFFMPEGError()
        return True
    return commands.check(predicate)
