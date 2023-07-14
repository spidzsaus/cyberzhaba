import discord

from app.db.models import SqlReactionRole
from app.db import database
from app.exceptions import AlreadyExists
from app.helper_tools import async_none_on_catch

class ReactionRole:
    id: int
    channel_id: int
    message_id: int
    reaction_id: int | None
    reaction_char: str | None
    role_id: int

    @classmethod
    def by_id(cls, rrid: int):
        db_sess = database.session()
        reaction_role = db_sess.query(SqlReactionRole).filter(
            SqlReactionRole.id == rrid
        ).first()
        return reaction_role and cls(reaction_role)

    @classmethod
    def search(cls, message: discord.Message, reaction: discord.Emoji | str):
        db_sess = database.session()
        query = db_sess.query(SqlReactionRole).filter(
            SqlReactionRole.channel_id == message.channel.id,
            SqlReactionRole.message_id == message.id,
        )
        match reaction:
            case discord.Emoji():
                query = query.filter(
                    SqlReactionRole.reaction_id == reaction.id
                )
            case _:
                query = query.filter(
                    SqlReactionRole.reaction_char == reaction
                )
        reaction_role = query.first()
        return reaction_role and cls(reaction_role)

    @classmethod
    def create(cls, message: discord.Message, reaction: discord.Emoji | str, role: discord.Role):
        db_sess = database.session()
        unique_test = cls.search(message, reaction)
        if unique_test:
            raise AlreadyExists('Reaction role already exists')

        reaction_role = SqlReactionRole(
            channel_id=message.channel.id,
            message_id=message.id,
            reaction_id=reaction.id if isinstance(reaction, discord.Emoji) else None,
            reaction_char=reaction if isinstance(reaction, str) else None,
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
        self.reaction_char = reaction_role.reaction_char
        self.role_id = reaction_role.role_id

    @async_none_on_catch(discord.NotFound)
    async def get_message(self, client: discord.Client) -> discord.Message:
        channel = await client.fetch_channel(self.channel_id)
        return await channel.fetch_message(self.message_id)

    @async_none_on_catch(discord.NotFound)
    async def get_role(self, client: discord.Client) -> discord.Role:
        channel = await client.fetch_channel(self.channel_id)
        return channel.guild.get_role(self.role_id)

    @async_none_on_catch(discord.NotFound)
    async def get_emoji(self, client: discord.Client) -> discord.Emoji | str:
        if self.reaction_char: return self.reaction_char
        channel = await client.fetch_channel(self.channel_id)
        return channel.guild.get_emoji(self.reaction_id)

    def __bool__(self):
        return True

    def sql(self, return_sess=False):
        db_sess = database.session()
        reaction_role = db_sess.query(SqlReactionRole).filter(SqlReactionRole.id == self.id).first()
        if return_sess:
            return (reaction_role, db_sess)
        return reaction_role
