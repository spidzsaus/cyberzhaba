from db.usermodel import SqlUser, SqlBarrellOrgan
from db import db_session
import discord
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
            organ = SqlBarrellOrgan(owner=owner.id, author=author)
            db_sess.add(organ)
            db_sess.commit()
        
        instance = object.__new__(cls)
        instance.__init__(organ)
        instance.owner_discord_id = owner_discord_id
        return instance

    def __init__(self, organ):
        self.name = organ.name
        self.description = organ.label
    
    @property
    def path(self):
        return os.path.join('data', 'barrellorgans', str(self.SQL().id))
    
    def preview(self):
        embed = discord.Embed(color=discord.Color.green(),
                              title='«' + self.name + '»',
                              description=self.description)

        image = discord.File(os.path.join(self.path, 'image.png'), filename="image.png")
        embed.set_image(url="attachment://image.png")

        return (embed, image)

    def __bool__(self):
        return True
    
    def SQL(self, return_sess=False):
        db_sess = db_session.create_session()
        owner = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.owner_discord_id
                                              ).first()
        organ = db_sess.query(SqlBarrellOrgan).filter(SqlBarrellOrgan.owner == owner.id
                                                      ).first()
        if return_sess:
            return (organ, db_sess)
        return organ
