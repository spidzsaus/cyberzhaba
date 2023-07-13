import sqlalchemy
from app.db.connection import SqlAlchemyBase


class SqlUser(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    discord_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    karma = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    blacklist = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    mod = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


class SqlBarrellOrgan(SqlAlchemyBase):
    __tablename__ = 'barrellorgans'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    author = sqlalchemy.Column(sqlalchemy.Integer)
    owner = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String)
    label = sqlalchemy.Column(sqlalchemy.Text)

class SqlReactionRole(SqlAlchemyBase):
    __tablename__ = 'reactionroles'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    channel_id = sqlalchemy.Column(sqlalchemy.Integer)
    message_id = sqlalchemy.Column(sqlalchemy.Integer)
    reaction_id = sqlalchemy.Column(sqlalchemy.Integer)
    role_id = sqlalchemy.Column(sqlalchemy.Integer)