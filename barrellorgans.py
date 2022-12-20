from data.usermodel import SqlUser, SqlBarrellOrgan
from data import db_session

class BarellOrgan:
    def __new__(cls, id):
        owner_discord_id = id
        db_sess = db_session.create_session()
        owner = db_sess.query(SqlUser).filter(SqlUser.discord_id == owner_discord_id
                                              ).first()
        if not owner:
            return None

        organ = db_sess.query(SqlBarrellOrgan).filter(SqlBarrellOrgan.owner == owner.id
                                                      ).first()
        
        if not organ:
            return None
        
        instance = cls(organ)
        return instance

    def __init__(self, organ):
        self.name = organ.name
        self.description = organ.label
        self.path = '/barrell-organs/' + self.name + '/'

    def __bool__(self):
        return True
    
    def SQL(self):
        return db_session.create_session().query(SqlUser).filter(
            SqlUser.discord_id == self.discord_id).first()
