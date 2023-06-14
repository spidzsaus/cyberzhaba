import discord
import json
import logging
import logging.handlers
import sys

logger = logging.getLogger('discord')
logging.getLogger('discord.http').setLevel(logging.INFO)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    


class EndDMSession(Exception):
    pass

class AccessDeniedError(Exception):
    pass

__Client__ = discord.Client(intents=discord.Intents.all())

class Config:
    def __init__(self, __config):
        for key, value in __config.items():
            self.__setattr__(key, value)
    

with open('config.json', encoding='utf-8') as file:
    __Config__ = Config(json.load(file))

if __Config__.debug_mode:
    from secret_data import DEBUG_TOKEN
    __Token__ = DEBUG_TOKEN
    logger.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    file_handler = logging.handlers.RotatingFileHandler(
        filename='debug.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

else:
    from secret_data import PROD_TOKEN
    __Token__ = PROD_TOKEN
    logger.setLevel(logging.INFO)
    file_handler = logging.handlers.RotatingFileHandler(
        filename='production.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    


__Commands__ = {}
__DMSessionOptions__ = {}
__ActiveDMSessions__ = {}


@__Client__.event
async def on_message(msg: discord.Message):
    if msg.author == __Client__.user:
        return
    
    if msg.channel.type is discord.ChannelType.private:
        if msg.author.id not in __ActiveDMSessions__:
            _session_started = False
            for keyword, sessiontype in __DMSessionOptions__.items():
                if msg.content.startswith(keyword):
                    __ActiveDMSessions__[msg.author.id] = sessiontype(msg)
                    _session_started = True
            if not _session_started:
                return
        try:
            await __ActiveDMSessions__[msg.author.id].feed(msg)
        except EndDMSession:
            del __ActiveDMSessions__[msg.author.id]

    
    else:
        if msg.content.startswith(__Config__.prefix):
            body = msg.content[len(__Config__.prefix):].strip().split()
            if not body: return
            for keyword, command in __Commands__.items():
                if body[0].lower() == keyword.lower():
                    try:
                        await command(msg)
                    except AccessDeniedError:
                        emb = discord.Embed(color=discord.Color.red(),
                                            title='Не-а!',
                                            description='Не ваша это команда.')
                        await msg.channel.send(embed=emb)

@__Client__.event
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
|\t"""
        )
    print('|\tSETUP FINISHED')
    print('|\tThe bot is running under @' + __Client__.user.name + '#' + __Client__.user.discriminator)
    print('|\t' + ('[!] ' if __Config__.debug_mode else '') + 'Debug mode is turned ' + ('ON' if __Config__.debug_mode else 'OFF'))
    print('\n')
    #User(408980792165924884).make_mod()

def command(keyword):
    def wrapper(func):
        __Commands__[keyword] = func
        return func
    return wrapper
        
class DMSession:
    def __init__(self, msg: discord.Message):
        self._next_step = self.first

    async def feed(self, msg: discord.Message):
        await self._next_step(msg)
    
    def stop(self, msg):
        raise EndDMSession

    def next(self, func):
        self._next_step = func

def dm_session(keyword):
    def wrapper(cls):
        __DMSessionOptions__[keyword] = cls
        return cls
    return wrapper

