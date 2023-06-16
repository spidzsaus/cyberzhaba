import traceback

import discord
from discord.ext import commands

from app.bot.dm_sessions import EndDMSession
from app.bot_logging import bot_logger
from app.helper_tools import basic_embed


class DMSessionsCog(commands.Cog):
    def __init__(self, bot, sessions: dict):
        self.bot = bot
        self.sessions = sessions
        self.active_sessions = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.type is not discord.ChannelType.private:
            return
        if message.author.id not in self.active_sessions:
            target_session = [
                session_type(message) for keyword, session_type 
                in self.sessions.items() if message.content.startswith(keyword)
            ][0]
            if target_session:
                self.active_sessions[message.author.id] = target_session
        try:
            await self.active_sessions[message.author.id].feed(message)
        except EndDMSession:
            del self.active_sessions[message.author.id]
        except Exception:
            bot_logger.error(
                'An error has occured in DM session with %s#%s (%s) (%s)',
                message.author.name, message.author.discriminator,
                message.author.global_name, message.author.id
            )
            bot_logger.error(traceback.format_exc())
            del self.active_sessions[message.author.id]
            embed = basic_embed(
                title=":x: кто-то сломал криптожабу. они за это заплатят.",
                text="программная ошибка в ЛС сессии. сессия была остановлена. простите.",
                color=discord.Color.red(),
            )
            await message.channel.send(embed=embed)
