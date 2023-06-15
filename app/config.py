import json
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
DEBUG = os.getenv("DEBUG", 'true') == 'true'

with open('server_config.json', encoding='utf-8') as file:
    logovo_config = json.load(file)
