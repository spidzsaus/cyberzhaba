import logging
import logging.handlers
import sys
from app.config import DEBUG

discord_logger = logging.getLogger('discord')
discord_client_logger = logging.getLogger('discord.client')
discord_gateway_logger = logging.getLogger('discord.gateway')
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
    for logger in (discord_gateway_logger, discord_client_logger, discord_http_logger, 
                   discord_logger, bot_logger):
        logger.setLevel(logging.DEBUG)
        logger.addHandler(stdout_handler)
        logger.addHandler(debug_file_handler)
else:
    for logger in (discord_gateway_logger, discord_client_logger, discord_http_logger, 
                   discord_logger, bot_logger):
        logger.setLevel(logging.INFO)
        logger.addHandler(production_file_handler)