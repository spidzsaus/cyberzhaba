import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

from app.bot_logging import bot_logger

SqlAlchemyBase = dec.declarative_base()

class DBConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.factory = None
        self.connected = False

    def connect(self):
        conn_str = f'sqlite:///{str(self.db_file).strip()}?check_same_thread=False'
        bot_logger.info("Establishing connection with %s", conn_str)

        engine = sa.create_engine(conn_str, echo=False)
        self.factory = orm.sessionmaker(bind=engine)

        # from app.db import usermodel

        SqlAlchemyBase.metadata.create_all(engine)

        self.connected = True

    def session(self) -> Session:
        if not self.connected:
            self.connect()
        return self.factory()
