from typing import Callable
import discord


class EndDMSession(Exception):
    pass


class DMSession:
    def __init__(self, _: discord.Message):
        self._next_step = self.first

    async def feed(self, msg: discord.Message):
        await self._next_step(msg)

    def stop(self, msg):
        raise EndDMSession

    def next(self, func):
        self._next_step = func

    async def first(self, msg):
        raise NotImplementedError


class CommandsManager:
    commands: dict[str, Callable]
    active_dm_sessions: dict[int, DMSession]
    dm_sessions: dict[str, type]

    def __init__(self):
        self.commands = dict()
        self.active_dm_sessions = dict()
        self.dm_sessions = dict()

    def command(self, keyword: str):
        def wrapper(func: Callable):
            self.commands[keyword] = func
            return func
        return wrapper

    def dm_session(self, keyword):
        def wrapper(cls):
            self.dm_sessions[keyword] = cls
            return cls
        return wrapper

    def get_command(self, keyword: str):
        keyword = keyword.lower()
        if keyword in self.commands:
            return self.commands[keyword]
        return None

    async def process_dm(self, msg: discord.Message):
        if msg.author.id not in self.active_dm_sessions:
            _session_started = False
            for keyword, sessiontype in self.dm_sessions.items():
                if msg.content.startswith(keyword):
                    self.active_dm_sessions[msg.author.id] = sessiontype(msg)
                    _session_started = True
            if not _session_started:
                return
        try:
            await self.active_dm_sessions[msg.author.id].feed(msg)
        except EndDMSession:
            del self.active_dm_sessions[msg.author.id]
