import os
import datetime
from dotenv import load_dotenv

load_dotenv()

TIMEZONE = datetime.timezone(datetime.timedelta(hours=3), "MSK")
TOKEN = os.getenv("TOKEN")
DEBUG = os.getenv("DEBUG", 'true') == 'true'
