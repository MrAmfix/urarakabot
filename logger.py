"""
This module provides enhanced logging capabilities using color-coded log messages
and API request logging for FastAPI routes.
"""

import logging
import inspect
from functools import wraps
from colorlog import ColoredFormatter
from datetime import datetime


class CustomColoredFormatter(ColoredFormatter):
    """
    A custom log formatter that applies color coding to log messages based on severity level.
    """

    def format(self, record):
        levelname = record.levelname
        if record.levelname == "DEBUG":
            return f"\033[37m{levelname:<8} {record.getMessage()}\033[0m"
        else:
            formatted_message = super().format(record)
            return formatted_message.replace(f"{levelname}:", f"{levelname:<8}")


# Configure logging handler with color formatting
handler = logging.StreamHandler()
formatter = CustomColoredFormatter(
    "%(log_color)s%(levelname)s:%(reset)s %(message)s",
    log_colors={
        "DEBUG": "white",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def _sub_search_logs(handler):

    @wraps(handler)
    async def wrapper(*args, **kwargs):
        bound_arguments = inspect.signature(handler).bind(*args, **kwargs).arguments

        log_text = ''
        user = None

        if 'message' in bound_arguments:
            user = bound_arguments['message'].from_user
        elif 'callback_query' in bound_arguments:
            user = bound_arguments['callback_query'].from_user

        log_text += f'Handler: {handler.__name__}'
        if user:
            log_text += f' | TelegramId: {user.id} | Username: {user.username}'

        try:
            logger.debug('----------------------------')
            logger.debug(f'TIME: {datetime.now()}')
            logger.info(log_text)
            return await handler(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            raise

    return wrapper


def search_logs(route_decorator):
    def wrapper(handler):
        wrapped_handler = _sub_search_logs(handler)
        return route_decorator(wrapped_handler)

    return wrapper