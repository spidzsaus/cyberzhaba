import json

import discord
from discord.ext import commands

from app.entities.guilds import Guild


class GuildConfigurationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_group(
        name="настройки-сервера"
    )
    @discord.app_commands.default_permissions(manage_guild=True)
    @commands.guild_only()
    async def server_config(self, ctx):
        if ctx.invoked_subcommand is None:
            raise commands.CommandNotFound()

    @server_config.command(
        "сет", description="поменять серверные настройки бота."
    )
    @discord.app_commands.rename(key="ключ", value="значение")
    @discord.app_commands.describe(
        key="настройка, которую нужно поменять",
        value="на что поменять настройку"
    )
    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    async def server_config_set(self, ctx, key: str, value: str | None):
        config = Guild(ctx.guild.id).config

        if value is None:
            del config[key]
        else:
            try:
                config[key] = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                config[key] = value

        await ctx.send(f"✅ `{key}` = `{config[key]}`")

    @server_config.command(
        "гет", description="получить серверные настройки бота."
    )
    @discord.app_commands.rename(key="ключ")
    @discord.app_commands.describe(
        key="настройка, которую нужно посмотреть (не указывайте, \
чтобы посмотреть весь конфиг)"
    )
    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    async def server_config_get(self, ctx, key: str | None):
        config = Guild(ctx.guild.id).config
        if key is None:
            await ctx.send(f"```{config}```")
        else:
            await ctx.send(f"👉 `{key}` = `{config[key]}`")
