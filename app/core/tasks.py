import logging
from core.models import Post
from celery import shared_task

from core.utils.log_handlers import LoggingHandler

logger = logging.getLogger(__name__)
logger.addHandler(LoggingHandler())
