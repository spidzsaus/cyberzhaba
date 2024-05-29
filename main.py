import asyncio

from alembic.config import Config
from alembic import command

from app import main

if __name__ == '__main__':
    # run database migrations
    alembic_cfg = Config('./alembic.ini')
    alembic_cfg.attributes['configure_logger'] = False
    command.upgrade(alembic_cfg, 'head')

    asyncio.run(main())
