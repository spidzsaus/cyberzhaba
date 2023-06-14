from config import cmd_manager
from bot.commands_exceptions import *
from db import db_session
from db.usermodel import SqlUser
from helper_tools import basic_embed
from users import User


@cmd_manager.command("блеклист")
async def blacklist(msg):
    if not User(msg.author.id).SQL().mod:
        raise AccessDeniedError
    args = msg.content.split()
    if len(args) == 1:
        db_sess = db_session.create_session()
        users = db_sess.query(SqlUser).filter(SqlUser.blacklist == True)
        embed = basic_embed(
            title="Чёрный список Криптожабы.", text="Вот они, сверху вниз:"
        )
        for i, user in enumerate(users):
            u = await User(user.discord_id).DISCORD()
            embed.add_field(name=str(i + 1) + ". " + u.name, value="_ _")
        await msg.channel.send(embed=embed)
    elif args[1] == "добавить":
        user = User(int(msg.content.split()[2]))
        user.add_to_blacklist()
        d = await user.DISCORD()
        embed = basic_embed(
            title=d.name + " добавлен в чёрный список.",
            text="Смейтесь его! Гоняйте над ним!",
        )
        if d.avatar:
            embed.set_thumbnail(url=d.avatar_url)
        await msg.channel.send(embed=embed)
    elif args[1] == "убрать":
        user = User(int(msg.content.split()[2]))
        user.remove_from_blacklist()
        d = await user.DISCORD()
        embed = basic_embed(
            title=d.name + " вычтен из чёрного списка.",
            text="на этот раз прощаем.",
        )
        if d.avatar:
            embed.set_thumbnail(url=d.avatar_url)
        await msg.channel.send(embed=embed)