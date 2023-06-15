import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

from app.bot_logging import bot_logger

SqlAlchemyBase = dec.declarative_base()

class DBConnection:
    def __init__(self, db_file):
        conn_str = f'sqlite:///{str(db_file).strip()}?check_same_thread=False'
        bot_logger.info("Establishing connection with %s", conn_str)

        engine = sa.create_engine(conn_str, echo=False)
        self.factory = orm.sessionmaker(bind=engine)

        # from app.db import usermodel

        SqlAlchemyBase.metadata.create_all(engine)

    def session(self) -> Session:
        return self.factory()
