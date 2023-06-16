from discord.ext import commands

from app.helper_tools import basic_embed


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name='хелп',
        description='справка.'
    )
    async def help_command(self, ctx):
        embed = basic_embed(
            "Справка",
            "**кж!карма** - посмотреть свой профиль.\n"
            "**кж!карма {пользователь}** - посмотреть чужой профиль.\n"
            "**кж!лидеры {страница}** - посмотреть список лидеров по карме.",
        )
        await ctx.send(embed=embed)
