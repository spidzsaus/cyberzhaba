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
