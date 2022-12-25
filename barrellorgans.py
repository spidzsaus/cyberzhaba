from db.usermodel import SqlUser, SqlBarrellOrgan
from db import db_session
import os

class BarellOrgan:
    def __new__(cls, id, init=False, author=None):
        owner_discord_id = id
        db_sess = db_session.create_session()
        owner = db_sess.query(SqlUser).filter(SqlUser.discord_id == owner_discord_id
                                              ).first()
        if not owner:
            return None

        organ = db_sess.query(SqlBarrellOrgan).filter(SqlBarrellOrgan.owner == owner.id
                                                      ).first()
        
        if not organ:
            if not init:
                return None
            organ = SqlBarrellOrgan(owner=owner.id, author=author.id)
            db_sess.add(organ)
            db_sess.commit()
        
        instance = cls(organ)
        instance.owner_discord_id = owner_discord_id
        return instance

    def __init__(self, organ):
        self.name = organ.name
        self.description = organ.label
    
    @property
    def path(self):
        return os.path.join('data', 'barrellorgans', str(self.SQL().id))

    def __bool__(self):
        return True
    
    def SQL(self):
        db_sess = db_session.create_session()
        owner = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.owner_discord_id
                                              ).first()
        organ = db_sess.query(SqlBarrellOrgan).filter(SqlBarrellOrgan.owner == owner.id
                                                      ).first()
        return organ
