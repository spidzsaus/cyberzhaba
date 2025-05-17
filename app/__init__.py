import os
import asyncio

import discord

from discord.ext import commands

import app.handlers
from app.bot_logging import bot_logger
from app.config import TOKEN

from app.bot.cogs.sysop_tools import SysOpToolsCog
from app.bot.cogs.help import HelpCog
from app.bot.cogs.special_events import SpecialEventsCog
from app.bot.cogs.economics import EconomicsCog
from app.bot.cogs.dm_sessions import DMSessionsCog
from app.bot.cogs.barrel_organs import BarrelOrgansCog
from app.bot.cogs.reactionroles import ReactionRolesCog
from app.bot.cogs.guild_config import GuildConfigurationCog
from app.bot.cogs.personal_roles import PersonalRolesCog
from app.bot.cogs.last_activity import LastActivityCog
from app.bot.cogs.birthdays import BirthdaysCog
from app.bot.cogs.mailbox import MailboxCog

from app.bot.dmsessions.compliment_oneliner import ComplimentOneliner
from app.bot.dmsessions.secret_santa import BarrellOrganCrafting

client = commands.Bot(
    command_prefix='кж!',
    intents=discord.Intents.all()
)


@client.event
async def on_ready():
    await app.handlers.on_ready(client)


async def main():
    async with client:
        if not os.path.exists('./data'):
            os.makedirs('./data')

        bot_logger.info('Booting up the discord client')

        client.add_listener(app.handlers.on_command_error)

        await client.add_cog(SysOpToolsCog(client))
        await client.add_cog(HelpCog(client))
        await client.add_cog(SpecialEventsCog(client))
        await client.add_cog(EconomicsCog(client))
        await client.add_cog(BarrelOrgansCog(client))
        await client.add_cog(ReactionRolesCog(client))
        await client.add_cog(DMSessionsCog(client,
            {
                "похвали меня": ComplimentOneliner,
                "создать шарманку!": BarrellOrganCrafting
            }
        ))
        await client.add_cog(GuildConfigurationCog(client))
        await client.add_cog(PersonalRolesCog(client))
        await client.add_cog(LastActivityCog(client))
        await client.add_cog(BirthdaysCog(client))
        await client.add_cog(MailboxCog(client))

        await client.start(TOKEN)
