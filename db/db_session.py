import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

from bot_logging import bot_logger

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    bot_logger.info(f"Establishing connection with {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()