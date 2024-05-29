import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
DEBUG = os.getenv("DEBUG", 'true') == 'true'
