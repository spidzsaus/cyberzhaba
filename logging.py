import logging
import sys

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
