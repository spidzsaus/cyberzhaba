from db.usermodel import SqlUser, SqlBarrellOrgan
from db import db_session

from hub import __Client__


class User:
    @classmethod
    def from_string(cls, string):
        try:
            return User(int(string))
        except ValueError:
            if string.startswith('<@!') and string[-1] == '>':
                return User(int(string[3:-1]))
        return False

    def __init__(self, id):
        self.discord_id = id
        
        db_sess = db_session.create_session()
        if not db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first():
            new = SqlUser(discord_id=id)
            db_sess.add(new)
            db_sess.commit()
        return None

    def __bool__(self):
        return True

    async def DISCORD(self):
        return await __Client__.fetch_user(self.discord_id)
    
    def SQL(self):
        return db_session.create_session().query(SqlUser).filter(
            SqlUser.discord_id == self.discord_id).first()
    
    def organ(self):
        return db_session.create_session().query(SqlBarrellOrgan).filter(
            SqlBarrellOrgan.owner == self.SQL().id).first()

    @property
    def karma(self):
        db_sess = db_session.create_session()
        return db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first().karma

    def is_blacklisted(self):
        db_sess = db_session.create_session()
        return db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first().blacklist

    def add_to_blacklist(self):
        db_sess = db_session.create_session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.blacklist = True
        db_sess.commit()

    def make_mod(self):
        db_sess = db_session.create_session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.mod = True
        db_sess.commit()

    def unmod(self):
        db_sess = db_session.create_session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.mod = False
        db_sess.commit()      

    def remove_from_blacklist(self):
        db_sess = db_session.create_session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.blacklist = False
        db_sess.commit()

    def add_karma(self, add):
        db_sess = db_session.create_session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.karma = user.karma + add
        db_sess.commit()