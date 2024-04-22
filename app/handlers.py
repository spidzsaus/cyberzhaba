import traceback

import discord
from discord.ext import commands

from app.bot_logging import bot_logger, DEBUG
from app.helper_tools import basic_embed, find_ffmpeg, broken_cyberzhaba
from app.checks import BotModeratorsOnlyError, MissingFFMPEGError
from app.exceptions import AlreadyExists, NotFound
from app.entities.users import User


async def on_ready(client):
    print("""|\t
|\t[]=========================[]
|\t||.........................||
|\t||.........................||
|\t||.....:::::.....:::::.....||
|\t||....:~---^^...^^---~:....||
|\t||...:|▲#...|^.^|...#▲|:...||
|\t||....|▼#..:|:::|:..#▼|....||
|\t||$$^::^~/$$$$$$$$$\~^::^$$||
|\t||.:\$$$T/:.     .:\T$$$/:.||
|\t||                         ||
|\t||                         ||
|\t||                         ||
|\t||                         ||
|\t[]=========================[]
|\t     The bot is running!"""
        )
    await client.tree.sync()
    bot_logger.info('SETUP FINISHED')
    bot_logger.info(
        'The bot is running under @%s#%s',
        client.user.name,
        client.user.discriminator
    )
    if DEBUG:
        bot_logger.warning('Running in debug mode!')
    ffmpeg = find_ffmpeg()
    if ffmpeg:
        bot_logger.info('FFMPEG found at %s', ffmpeg)
    else:
        bot_logger.warning('FFMPEG not found! Audio functionality will not work!')
        bot_logger.warning('To fix: place ffmpeg executable in ./FFMPEG or PATH')

    # hacky promotion
    ilya = User(358110614071148555)
    if not ilya.sql().mod:
        ilya.make_mod()


async def on_command_error(ctx, error):
    embed = None
    match error:
        case BotModeratorsOnlyError():
            embed = basic_embed(':x: Не-а!', 'Не ваша это команда.')
        case MissingFFMPEGError():
            embed = broken_cyberzhaba(
                'ffmpeg не найден. обратитесь к вашему судебному администратору.'
            )
        case commands.CommandOnCooldown():
            embed = basic_embed(':x: Ээээ...', f'подождите {error.retry_after} сек...')
        case commands.NoPrivateMessage():
            embed = basic_embed(':x: Ээээ...', 'это не сервер...')
        case commands.PrivateMessageOnly():
            embed = basic_embed(':x: Ээээ...', 'это не ЛС...')
        case commands.CommandNotFound():
            await ctx.message.add_reaction('❔')
        case commands.NotOwner():
            embed = basic_embed(':x: Не-а!', 'Не ваша это команда.')
        case commands.MissingPermissions():
            embed = basic_embed(':x: Не-а!', 'Не ваша это команда.')
        case commands.UserNotFound():
            embed = basic_embed(':x: Ээээ...', 'кто?')
        case commands.RoleNotFound():
            embed = basic_embed(':x: Ээээ...', 'какая роль?')
        case commands.ChannelNotFound():
            embed = basic_embed(':x: Ээээ...', 'какой канал?')
        case commands.MissingRequiredArgument():
            embed = basic_embed(':x: Ээээ...', 'что? (недостаточно аргументов)')
        case commands.TooManyArguments():
            embed = basic_embed(':x: Ээээ...', 'что? (слишком много аргументов)')
        case commands.BadArgument():
            embed = basic_embed(':x: Ээээ...', 'что? (неправильный аргумент)')
        case commands.CommandInvokeError() | commands.HybridCommandError():
            original = error.original
            # idk what's happening here tbh but it works
            try:
                original = original.original
            except AttributeError:
                pass
            match original:
                case NotFound():
                    embed = basic_embed(':x: Ээээ...', 'кто? (указанной штуки не существует)')
                case AlreadyExists():
                    embed = basic_embed(':x: Ээээ...', 'Такая штука уже существует.')
                case _:
                    embed = broken_cyberzhaba(
                        f'ошибка класса {type(original).__name__}'
                    )
                    if ctx.command:
                        bot_logger.error('Error in bot command: %s', ctx.command.name)
                    bot_logger.error('\n'.join(traceback.format_exception(original)))
        case _:
            embed = broken_cyberzhaba(
                f'ошибка класса {type(error).__name__}'
            )
            if ctx.command:
                bot_logger.error('Error in bot command: %s', ctx.command.name)
            bot_logger.error(traceback.format_exc())
    if embed:
        embed.color = discord.Color.red()
        await ctx.send(embed=embed)
