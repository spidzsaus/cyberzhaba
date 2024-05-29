from sqlalchemy.orm.attributes import flag_modified    

from app.db.models import SqlGuild
from app.db import database


class GuildConfig:
    def __init__(self, guild):
        self.guild = guild

    def get(self, key, default=None):
        try:
            result = self.guild.sql().config[key]
        except KeyError:
            return default
        return result

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        db_sess = database.session()
        sql_guild = db_sess.get(SqlGuild, self.guild.discord_id)
        sql_guild.config[key] = value
        flag_modified(sql_guild, "config")
        db_sess.commit()

    def __delitem__(self, key):
        db_sess = database.session()
        sql_guild = db_sess.get(SqlGuild, self.guild.discord_id)
        del sql_guild.config[key]
        flag_modified(sql_guild, "config")
        db_sess.commit()

    def __str__(self):
        return str(self.guild.sql().config)

class Guild:
    def __init__(self, uid):
        self.discord_id = uid

        db_sess = database.session()
        if not db_sess.get(SqlGuild, uid):
            new = SqlGuild(discord_id=uid)
            db_sess.add(new)
            db_sess.commit()

    def __bool__(self):
        # is this necessary?
        return True

    def sql(self) -> SqlGuild:
        return database.session().get(SqlGuild, self.discord_id)

    @property
    def config(self) -> GuildConfig:
        return GuildConfig(self)
