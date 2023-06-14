import os

from config import *
from setup import *
from db import db_session
from bot_logging import bot_logger


if __name__ == '__main__':
    db_session.global_init(os.path.join('data', 'botdata.db'))
    bot_logger.info('Booting up the discord client')
    client.run(TOKEN)