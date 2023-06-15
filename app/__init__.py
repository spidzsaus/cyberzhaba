import os
import discord
from discord.ext import commands

from app.bot_logging import bot_logger
from app.config import TOKEN
from app.db.connection import DBConnection

client = commands.Bot(
    command_prefix='кж!',
    intents=discord.Intents.all()
)


if __name__ == '__main__':
    if not os.path.exists('./data'):
        os.makedirs('./data')
    database = DBConnection(os.path.join('.', 'data', 'botdata.db'))
    bot_logger.info('Booting up the discord client')
    client.run(TOKEN, log_handler=None)
