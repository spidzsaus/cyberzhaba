from app import database
from app.bot.commands_exceptions import AccessDeniedError
from app.db.usermodel import SqlUser
from app.helper_tools import basic_embed
from app.entities.users import User
from app.config import cmd_manager


@cmd_manager.command("блеклист")
async def blacklist(msg):
    if not User(msg.author.id).sql().mod:
        raise AccessDeniedError
    args = msg.content.split()
    if len(args) == 1:
        db_sess = database.session()
        users = db_sess.query(SqlUser).filter(SqlUser.blacklist == True)
        embed = basic_embed(
            title="Чёрный список Криптожабы.", text="Вот они, сверху вниз:"
        )
        for i, user in enumerate(users):
            user = await User(user.discord_id).discord()
            embed.add_field(name=str(i + 1) + ". " + user.name, value="_ _")
        await msg.channel.send(embed=embed)
    elif args[1] == "добавить":
        user = User(int(msg.content.split()[2]))
        user.add_to_blacklist()
        discord_user = await user.discord()
        embed = basic_embed(
            title=discord_user.name + " добавлен в чёрный список.",
            text="Смейтесь его! Гоняйте над ним!",
        )
        if discord_user.avatar:
            embed.set_thumbnail(url=discord_user.avatar_url)
        await msg.channel.send(embed=embed)
    elif args[1] == "убрать":
        user = User(int(msg.content.split()[2]))
        user.remove_from_blacklist()
        discord_user = await user.discord()
        embed = basic_embed(
            title=discord_user.name + " вычтен из чёрного списка.",
            text="на этот раз прощаем.",
        )
        if discord_user.avatar:
            embed.set_thumbnail(url=discord_user.avatar_url)
        await msg.channel.send(embed=embed)
