import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class SqlUser(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    discord_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    karma = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    blacklist = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    mod = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

class SqlBarrellOrgan(SqlAlchemyBase):
    __tablename__ = 'organs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    author = sqlalchemy.ForeignKey(SqlUser.id)
    owner = sqlalchemy.ForeignKey(SqlUser.id)
    name = sqlalchemy.Column(sqlalchemy.String)
    label = sqlalchemy.Column(sqlalchemy.Text)