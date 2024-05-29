from app.db.models import SqlMembership
from app.entities.users import User
from app.entities.guilds import Guild
from app.db import database


class Membership:
    def __init__(self, user_id, guild_id):
        self.user_id = user_id
        self.guild_id = guild_id

        # this ensures these actually exist -
        # avoiding foreign key errors!
        User(user_id)
        Guild(guild_id)

        db_sess = database.session()
        sql_membership = db_sess.query(SqlMembership).filter(
            SqlMembership.user == user_id, SqlMembership.guild == guild_id
        ).first()
        if not sql_membership:
            sql_membership = SqlMembership(user=user_id, guild=guild_id)
            db_sess.add(sql_membership)
            db_sess.commit()

        self.id = sql_membership.id

    def __bool__(self):
        # is this necessary?
        return True

    def sql(self) -> SqlMembership:
        return database.session().get(SqlMembership, self.id)

    @property
    def karma(self):
        return self.sql().karma

    def add_karma(self, amount):
        db_sess = database.session()
        membership = db_sess.get(SqlMembership, self.id)
        membership.karma += amount
        db_sess.commit()
