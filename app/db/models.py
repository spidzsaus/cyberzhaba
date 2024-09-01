import sqlalchemy
from app.db.connection import SqlAlchemyBase


class SqlGuild(SqlAlchemyBase):
    __tablename__ = 'guilds'

    discord_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    # JSON is a non-universal type (requires database support), but
    # it works on Sqlite, PostgresSQL and MySQL, and i honestly
    # don't know what other db we could possibly use for this
    config = sqlalchemy.Column(sqlalchemy.JSON, default={})


class SqlUser(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    discord_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    blacklist = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    mod = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    last_activity = sqlalchemy.Column(sqlalchemy.DateTime)
    last_activity_type = sqlalchemy.Column(sqlalchemy.String, default="")


class SqlMembership(SqlAlchemyBase):
    __tablename__ = 'memberships'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user = sqlalchemy.Column(sqlalchemy.ForeignKey(SqlUser.discord_id))
    guild = sqlalchemy.Column(sqlalchemy.ForeignKey(SqlGuild.discord_id))

    karma = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    last_activity = sqlalchemy.Column(sqlalchemy.DateTime)
    last_activity_type = sqlalchemy.Column(sqlalchemy.String, default="")


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
    reaction_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    reaction_char = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    role_id = sqlalchemy.Column(sqlalchemy.Integer)
