import discord

from app.db.models import SqlReactionRole
from app.db import database
from app.exceptions import AlreadyExists


class ReactionRole:
    id: int
    channel_id: int
    message_id: int
    reaction_id: int
    role_id: int

    @classmethod
    def search(cls, message: discord.Message, reaction: discord.Emoji):
        db_sess = database.session()
        reaction_role = db_sess.query(SqlReactionRole).filter(
            SqlReactionRole.channel_id == message.channel.id,
            SqlReactionRole.message_id == message.id,
            SqlReactionRole.reaction_id == reaction.id
        )
        return reaction_role

    @classmethod
    def create(cls, message: discord.Message, reaction: discord.Emoji, role: discord.Role):
        db_sess = database.session()
        unique_test = cls.search(message, reaction)
        if unique_test:
            raise AlreadyExists('Reaction role already exists')

        reaction_role = SqlReactionRole(
            channel_id=message.channel.id,
            message_id=message.id,
            reaction_id=reaction.id,
            role_id=role.id 
        )
        db_sess.add(reaction_role)
        db_sess.commit()

        instance = cls(reaction_role)
        return instance

    def __init__(self, reaction_role: SqlReactionRole):
        self.id = reaction_role.id
        self.channel_id = reaction_role.channel_id
        self.message_id = reaction_role.message_id
        self.reaction_id = reaction_role.reaction_id
        self.role_id = reaction_role.role_id

    async def get_message(self, client: discord.Client):
        return await client.fetch_channel(self.channel_id).fetch_message(self.message_id)

    async def get_role(self, client: discord.Client):
        return await client.fetch_channel(self.channel_id).guild.get_role(self.role_id)

    def __bool__(self):
        return True

    def sql(self, return_sess=False):
        db_sess = database.session()
        reaction_role = db_sess.query(SqlReactionRole).filter(SqlReactionRole.id == self.id).first()
        if return_sess:
            return (reaction_role, db_sess)
        return reaction_role
