import secrets
import traceback
import aiohttp
import discord
from discord.ext import commands

from app import config
from app.entities.mailboxes import Mailbox
from app.entities.users import User
from app.entities.memberships import Membership
from app.db import database
from app.db.models import SqlMailbox
from app.helper_tools import basic_embed, determine_personal_role
from app.bot_logging import bot_logger
from app.checks import is_bot_moderator


class MailboxCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="почта", fallback="создать",
        description="создать почтовый ящик."
    )
    @discord.app_commands.rename(local_part="юзернейм")
    @discord.app_commands.describe(
        local_part="юзернейм (часть до собаки)"
    )
    async def mailbox(self, ctx, local_part: str):
        if not config.MAILBOX_DOMAIN or \
           not config.MAILCOW_SERVER or \
           not config.MAILCOW_TOKEN:
            await ctx.send(embed=basic_embed(
                ":x: хост забыл настроить функцию",
                "тыкни его об этом..",
                color=discord.Color.red()
            ), ephemeral=True)
            return

        if len(local_part) > 32:
            await ctx.send(embed=basic_embed(
                ":x: слишком длинный ник",
                "максимум 32 символа.",
                color=discord.Color.red()
            ), ephemeral=True)
            return

        user = User(ctx.author.id)
        membership = Membership(ctx.author.id, ctx.guild.id)
        if membership.sql().karma < 1 and \
           not determine_personal_role(ctx.author):
            await ctx.send(embed=basic_embed(
                ":x: слишком новый логовец",
                "получи как минимум 1 карму, или обратись к админу.",
                color=discord.Color.red()
            ), ephemeral=True)
            return

        db_sess = database.session()
        owned_mailboxes = db_sess.query(SqlMailbox).filter(
            SqlMailbox.user == user.discord_id
        ).all()
        max_mailboxes = user.sql().max_mailboxes or 1
        if len(owned_mailboxes) >= max_mailboxes:
            await ctx.send(embed=basic_embed(
                ":x: слишком много ящиков",
                f"максимум {max_mailboxes} на этом аккаунте.",
                color=discord.Color.red()
            ), ephemeral=True)
            return

        try:
            await ctx.author.send("создаю почтовый ящик...")
        except Exception:
            await ctx.send(embed=basic_embed(
                ":x: лс закрыты",
                f"открой ЛС, чтобы я могла тебе прислать данные от ящика!",
                color=discord.Color.red()
            ), ephemeral=True)
            return

        await ctx.send("загляни в личку", ephemeral=True)

        try:
            mailbox = Mailbox.create(
                user.discord_id,
                config.MAILBOX_DOMAIN,
                local_part=local_part
            )
        except NameError:
            await ctx.send(embed=basic_embed(
                ":x: такой ящик уже существует",
                f"попробуй придумать другой ник",
                color=discord.Color.red()
            ), ephemeral=True)
            return

        password = (
            "YouShouldChangeYourPasswordNOW!_"
            + secrets.token_urlsafe(8)
        )
        url = f"https://{config.MAILCOW_SERVER}/api/v1/add/mailbox"
        auth_header = {"X-API-Key": config.MAILCOW_TOKEN}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json={
                    "active": "1",
                    "domain": mailbox.domain,
                    "local_part": mailbox.local_part,
                    "name": "",
                    "authsource": "mailcow",
                    "password": password,
                    "password2": password,
                    "quota": 10240,
                    "force_pw_update": "1",
                    "tls_enforce_in": "0",
                    "tls_enforce_out": "0",
                    "tags": []
                }, headers=auth_header) as resp:
                    if resp.status != 200 or \
                        (await resp.json())[0]["type"] != "success":
                        await ctx.author.send(embed=basic_embed(
                            ":x: что-то пошло не так",
                            f"сервер вернул ошибку, попробуй позже.",
                            color=discord.Color.red()
                        ))
                        mailbox.delete()
                        return
            except aiohttp.ClientConnectionError as e:
                bot_logger.error(traceback.format_exc())
                await ctx.author.send(embed=basic_embed(
                    ":x: что-то пошло не так",
                    f"ошибка подключения к серверу, попробуй позже.",
                    color=discord.Color.red()
                ))
                mailbox.delete()
                return

        await ctx.author.send(f"""
**Почтовый ящик создан!**

`{local_part}@{config.MAILBOX_DOMAIN}`
пароль: `{password}`

Веб-почта находится здесь: https://{config.MAILCOW_SERVER}.
Зайди сейчас, чтобы поменять пароль со временного!

**Просьба использовать почту цивилизованно,** ибо более широкий интернет, и я не хочу, чтобы меня отменили твиттер-стайл (я хост, я несу за всех ответственность). Логовцы, вроде, и так этим не промышляют, но чур никого не обижать и не дискриминировать. И не используйте слюры!

По настройке клиентов: твой почтовый клиент должен сразу определить, какой сервер использовать, когда ты введёшь адрес и пароль. Если, однако, этого не случится, то используй следующие адреса:

SMTPS: `{config.MAILCOW_SERVER}:465`
IMAPS: `{config.MAILCOW_SERVER}:993`

Полную справку можно найти здесь: https://docs.mailcow.email/client/client-manual/

Хорошего дня!
        """.strip(), suppress_embeds=True)

    @commands.hybrid_group(name="почта-адм")
    @is_bot_moderator()
    async def mailbox_adm(self, ctx):
        pass

    @mailbox_adm.command(
        name="установить-лимит",
        description="поменять чей-то лимит на почтовые ящики."
    )
    @discord.app_commands.rename(discord_user="юзер", limit="лимит")
    @is_bot_moderator()
    async def set_mailbox_limit(self, ctx, 
                                discord_user: discord.User, limit: int):
        user = User(discord_user.id)
        user.set_mailbox_limit(limit)
        await ctx.send("Успех!")
