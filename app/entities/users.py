from datetime import datetime, date

from app.db.models import SqlUser, SqlBarrellOrgan
from app.db import database


class User:
    @classmethod
    def from_string(cls, string):
        try:
            return User(int(string))
        except ValueError:
            if string.startswith('<@!') and string[-1] == '>':
                return User(int(string[3:-1]))
        return False

    def __init__(self, uid):
        self.discord_id = uid

        db_sess = database.session()
        if not db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first():
            new = SqlUser(discord_id=uid)
            db_sess.add(new)
            db_sess.commit()

    def __bool__(self):
        return True

    def sql(self):
        return database.session().query(SqlUser).filter(
            SqlUser.discord_id == self.discord_id).first()

    def organ(self):
        return database.session().query(SqlBarrellOrgan).filter(
            SqlBarrellOrgan.owner == self.sql().id).first()

    def is_blacklisted(self):
        db_sess = database.session()
        return db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first().blacklist

    def add_to_blacklist(self):
        db_sess = database.session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.blacklist = True
        db_sess.commit()

    def make_mod(self):
        db_sess = database.session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.mod = True
        db_sess.commit()

    def unmod(self):
        db_sess = database.session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.mod = False
        db_sess.commit()

    def remove_from_blacklist(self):
        db_sess = database.session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.blacklist = False
        db_sess.commit()

    def mark_activity(self, activity_type: str):
        db_sess = database.session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.last_activity = datetime.now()
        user.last_activity_type = activity_type
        db_sess.commit()

    def set_birthday(self, birthday: date):
        db_sess = database.session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.birthday = birthday
        db_sess.commit()
