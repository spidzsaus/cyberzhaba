import json
import discord

import os
from dotenv import load_dotenv
load_dotenv()

from app.bot.commands_manager import CommandsManager

TOKEN = os.getenv("TOKEN")
DEBUG = os.getenv("DEBUG", 'true') == 'true'

class AttrDict:
    def __init__(self, __dict):
        for key, value in __dict.items():
            self.__setattr__(key, value)

with open('server_config.json', encoding='utf-8') as file:
    logovo_config = AttrDict(json.load(file))

cmd_manager = CommandsManager()
client = discord.Client(intents=discord.Intents.all())
