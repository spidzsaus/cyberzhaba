import os

from app.bot_logging *
from app.config import *
from app.handlers import *
from app.db import db_session


if __name__ == '__main__':
    db_session.global_init(os.path.join('data', 'botdata.db'))
    bot_logger.info('Booting up the discord client')
    client.run(TOKEN, log_handler=None)