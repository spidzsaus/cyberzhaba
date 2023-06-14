import os

from config import *
from setup import *
from db import db_session


if __name__ == '__main__':
    db_session.global_init(os.path.join('data', 'botdata.db'))
    print('|\tBooting up the discord client')
    client.run(TOKEN)