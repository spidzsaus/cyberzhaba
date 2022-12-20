import discord
import json

class EndDMSession(Exception):
    pass

class AccessDeniedError(Exception):
    pass

__Client__ = discord.Client(intents=discord.Intents.all())

class Config:
    def __init__(self, __config):
        for key, value in __config:
            self.__setattr__(key, value)
    

with open('config.json', encoding='utf-8') as file:
    __Config__ = Config(json.load(file))

if __Config__.debug_mode:
    from secret_data import DEBUG_TOKEN
    __Token__ = DEBUG_TOKEN
else:
    from secret_data import PROD_TOKEN
    __Token__ = PROD_TOKEN


__Commands__ = {}
__DMSessionOptions__ = {}
__ActiveDMSessions__ = {}


@__Client__.event
async def on_message(msg: discord.Message):
    if msg.author == __Client__.user:
        return
    
    if msg.channel.type is discord.ChannelType.private:
        if msg.author.id in __ActiveDMSessions__:
            try:
                await __ActiveDMSessions__[msg.author.id].feed(msg)
            except EndDMSession:
                del __ActiveDMSessions__[msg.author.id]

        for keyword, sessiontype in __DMSessionOptions__.items():
            if msg.startswith(keyword):
                __ActiveDMSessions__[msg.author.id] = await sessiontype(msg)
    
    else:
        if msg.content.startswith(__Config__.prefix):
            body = msg.content.lstrip(__Config__.prefix).strip().split()
            if not body: return
            for keyword, command in __Commands__.items():
                if body[0].lower() == keyword:
                    try:
                        await command(msg)
                    except AccessDeniedError:
                        emb = discord.Embed(color=discord.Color.red(),
                                            title='Не-а!',
                                            description='Не ваша это команда.')
                        await msg.channel.send(embed=emb)

def command(keyword):
    def wrapper(func):
        __Commands__[keyword] = func
        return func
    return wrapper
        
