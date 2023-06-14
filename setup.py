import discord

from config import *
import all_modules
from bot.commands_exceptions import AccessDeniedError
from bot.commands_manager import EndDMSession
from users import User
from bot_logging import bot_logger


@client.event
async def on_message(msg: discord.Message):
    if msg.author == client.user:
        return
    
    if msg.channel.type is discord.ChannelType.private:
        await cmd_manager.process_dm(msg)
    else:
        if msg.content.startswith(logovo_config.prefix):
            body = msg.content[len(logovo_config.prefix):].strip().split()
            if not body: return
            command = cmd_manager.get_command(body[0])
            if command:
                try:
                    await command(msg)
                except AccessDeniedError:
                    emb = discord.Embed(color=discord.Color.red(),
                                        title='Не-а!',
                                        description='Не ваша это команда.')
                    await msg.channel.send(embed=emb)
                    

@client.event
async def on_ready():
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
    bot_logger.info('SETUP FINISHED')
    bot_logger.info('The bot is running under @' + client.user.name + '#' + client.user.discriminator)
    bot_logger.info(('[!] ' if DEBUG else '') + 'Debug mode is turned ' + ('ON' if DEBUG else 'OFF'))
    #User(408980792165924884).make_mod()

async def reaction_event(payload, meaning=1):
    channel = await client.fetch_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    if msg.webhook_id:
        return
    user = await client.fetch_user(payload.user_id)
    if user.id == msg.author.id or user.bot or msg.author.bot:
        return
    
    category_whitelisted = channel.category and (channel.category_id in logovo_config.category_whitelist)
    channel_whitelisted = payload.channel_id in logovo_config.channel_whitelist
    keyword_whitelisted = True in [word in channel.name for word in logovo_config.channel_whitelist_keywords]

    if not (category_whitelisted or channel_whitelisted or keyword_whitelisted):
        return
    if User(payload.user_id).is_blacklisted() or User(msg.author.id).is_blacklisted():
        return
   # if days_delta(msg) >= CONFIG['message_expiration_date']:
   #     return
    if payload.emoji.id in logovo_config.praise:
        user = User(msg.author.id)
        user.add_karma(logovo_config.coeff * meaning)

@client.event
async def on_raw_reaction_add(payload):
    await reaction_event(payload, 1)

@client.event
async def on_raw_reaction_remove(payload):
    await reaction_event(payload, -1)