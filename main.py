import discord
from hub import __Client__, __Config__, __Token__
from users import User
from barrellorgans import BarellOrgan

from db import db_session

import bot.commands
import bot.dmsessions

async def reaction_event(payload, meaning=1):
    channel = await __Client__.fetch_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    if msg.webhook_id:
        return
    user = await __Client__.fetch_user(payload.user_id)
    if user.id == msg.author.id or user.bot or msg.author.bot:
        return
    if payload.channel_id not in __Config__.channel_whitelist and True not in [word in channel.name for word in __Config__.channel_whitelist_keywords]:
        return
    if User(payload.user_id).is_blacklisted() or User(msg.author.id).is_blacklisted():
        return
   # if days_delta(msg) >= CONFIG['message_expiration_date']:
   #     return
    if payload.emoji.id in __Config__.praise:
        user = User(msg.author.id)
        user.add_karma(__Config__.coeff * meaning)

@__Client__.event
async def on_raw_reaction_add(payload):
    await reaction_event(payload, 1)

@__Client__.event
async def on_raw_reaction_remove(payload):
    await reaction_event(payload, -1)

if __name__ == '__main__':
    db_session.global_init('botdata.db')
    print('|\tBooting up the discord client')
    __Client__.run(__Token__)
    