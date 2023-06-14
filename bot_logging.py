import logging
import sys
from config import DEBUG

discord_logger = logging.getLogger('discord')
discord_http_logger = logging.getLogger('discord.http')
bot_logger = logging.getLogger('bot')


dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')


stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)


debug_file_handler = logging.handlers.RotatingFileHandler(
    filename='debug.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
)
debug_file_handler.setFormatter(formatter)


production_file_handler = logging.handlers.RotatingFileHandler(
        filename='production.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
    )
production_file_handler.setFormatter(formatter)


if DEBUG:
    discord_http_logger.setLevel(logging.DEBUG)
    discord_logger.setLevel(logging.DEBUG)
    bot_logger.setLevel(logging.DEBUG)
    discord_http_logger.addHandler(stdout_handler)
    discord_http_logger.addHandler(debug_file_handler)
    discord_logger.addHandler(stdout_handler)
    discord_logger.addHandler(debug_file_handler)
    bot_logger.addHandler(stdout_handler)
    bot_logger.addHandler(debug_file_handler)
else:
    discord_http_logger.setLevel(logging.INFO)
    discord_logger.setLevel(logging.INFO)
    bot_logger.setLevel(logging.INFO)
    discord_http_logger.addHandler(production_file_handler)
    discord_logger.addHandler(production_file_handler)
    bot_logger.addHandler(production_file_handler)