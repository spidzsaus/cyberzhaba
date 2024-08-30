import discord
from discord.ext import commands

from app.helper_tools import determine_personal_role, basic_embed, broken_cyberzhaba

class PersonalRolesCog(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="переделатьроль",
        description="поменять цвет и/или название личной роли"
    )
    @discord.app_commands.rename(
        name="название", color="цвет"
    )
    @discord.app_commands.describe(
        name="новое название роли.", color="цвет роли."
    )
    @commands.guild_only()
    async def customize_personal_role(
        self, ctx, name: str | None, color: str | None
    ):
        role = determine_personal_role(ctx.author)
        values = {}
        if role is None:
            await ctx.send(
                embed=basic_embed(
                    ":x: не удалось найти роль",
                    "если у вас она действительно есть, позовите илью",
                    color=discord.Color.red()
                )
            )
            return

        if color is not None:
            try:
                color = discord.Color.from_str(color)
            except ValueError:
                await ctx.send(
                    embed=basic_embed(
                        ":x: неправильный цвет",
                        "попробуйте указать HEX цвет, вроде #77ff77",
                        color=discord.Color.red()
                    )
                )
                return
            values['color'] = color

        if name is not None:
            values['name'] = name

        if len(values) > 0:
            try:
                await role.edit(**values)
            except Exception as err:
                await ctx.send(
                    embed=broken_cyberzhaba(
                        "не удалось отредактировать роль"
                    )
                )
                return
            await ctx.send(embed=basic_embed(
                None, "✅ Успех!"
            ))
        else:
            await ctx.send(
                embed=basic_embed(
                    None, "❔ а что редактировать то собственно?",
                    color=discord.Color.yellow()
                )
            )
