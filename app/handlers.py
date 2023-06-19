import traceback

import discord
from discord.ext import commands

from app.bot_logging import bot_logger, DEBUG
from app.helper_tools import basic_embed, find_ffmpeg, broken_cyberzhaba
from app.checks import BotModeratorsOnlyError, MissingFFMPEGError


# @client.event
# async def on_message(msg: discord.Message):
#     if msg.author == client.user:
#         return

#     if msg.channel.type is discord.ChannelType.private:
#         await cmd_manager.process_dm(msg)
#     else:
#         if msg.content.startswith(logovo_config.prefix):
#             body = msg.content[len(logovo_config.prefix):].strip().split()
#             if not body: return
#             command = cmd_manager.get_command(body[0])
#             if command:
#                 try:
#                     await command(msg)
#                 except AccessDeniedError:
#                     emb = discord.Embed(color=discord.Color.red(),
#                                         title='Не-а!',
#                                         description='Не ваша это команда.')
#                     await msg.channel.send(embed=emb)


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


async def on_command_error(ctx, error):
    embed = None
    if isinstance(error, BotModeratorsOnlyError):
        embed = basic_embed(':x: Не-а!', 'Не ваша это команда.')
    elif isinstance(error, MissingFFMPEGError):
        embed = broken_cyberzhaba(
            'ffmpeg не найден. обратитесь к вашему судебному администратору.'
        )
    elif isinstance(error, commands.CommandOnCooldown):
        embed = basic_embed(':x: Ээээ...', f'подождите {error.retry_after} сек...')
    elif isinstance(error, commands.NoPrivateMessage):
        embed = basic_embed(':x: Ээээ...', 'это не сервер...')
    elif isinstance(error, commands.PrivateMessageOnly):
        embed = basic_embed(':x: Ээээ...', 'это не ЛС...')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction('❔')
    elif isinstance(error, commands.NotOwner):
        embed = basic_embed(':x: Не-а!', 'Не ваша это команда.')
    elif isinstance(error, commands.MissingPermissions):
        embed = basic_embed(':x: Не-а!', 'Не ваша это команда.')
    elif isinstance(error, commands.UserNotFound):
        embed = basic_embed(':x: Ээээ...', 'кто?')
    elif isinstance(error, commands.RoleNotFound):
        embed = basic_embed(':x: Ээээ...', 'какая роль?')
    elif isinstance(error, commands.ChannelNotFound):
        embed = basic_embed(':x: Ээээ...', 'какой канал?')
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = basic_embed(':x: Ээээ...', 'что? (недостаточно аргументов)')
    elif isinstance(error, commands.TooManyArguments):
        embed = basic_embed(':x: Ээээ...', 'что? (слишком много аргументов)')
    elif isinstance(error, commands.BadArgument):
        embed = basic_embed(':x: Ээээ...', 'что? (неправильный аргумент)')
    elif isinstance(error, commands.CommandInvokeError) or \
         isinstance(error, commands.HybridCommandError):
        embed = broken_cyberzhaba(
            f'ошибка класса {type(error.original).__name__}'
        )
        if ctx.command:
            bot_logger.error('Error in bot command: %s', ctx.command.name)
        bot_logger.error('\n'.join(traceback.format_exception(error.original)))
    else:
        embed = broken_cyberzhaba(
            f'ошибка класса {type(error).__name__}'
        )
        if ctx.command:
            bot_logger.error('Error in bot command: %s', ctx.command.name)
        bot_logger.error(traceback.format_exc())
    if embed:
        embed.color = discord.Color.red()
        await ctx.send(embed=embed)
