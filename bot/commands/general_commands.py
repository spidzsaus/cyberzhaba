from config import cmd_manager
from helper_tools import basic_embed

@cmd_manager.command("хелп")
async def help(msg):
    embed = basic_embed(
        "Справка",
        "**кж!карма** - посмотреть свой профиль.\n"
        "**кж!карма {пользователь}** - посмотреть чужой профиль.\n"
        "**кж!лидеры {страница}** - посмотреть список лидеров по карме.",
    )
    await msg.channel.send(embed=embed)