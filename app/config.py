import os
import datetime
from dotenv import load_dotenv

load_dotenv()

TIMEZONE = datetime.timezone(datetime.timedelta(hours=3), "MSK")
TOKEN = os.getenv("TOKEN")
DEBUG = os.getenv("DEBUG", 'true') == 'true'

MAILCOW_SERVER = os.getenv("MAILCOW_SERVER")
MAILCOW_TOKEN = os.getenv("MAILCOW_TOKEN")
MAILBOX_DOMAIN = os.getenv("MAILBOX_DOMAIN")