import logging
import sys
from google.cloud.logging_v2.handlers import StructuredLogHandler

def cloud_logging_settings() -> None:
    logger = logging.getLogger()
    logger.addHandler(StructuredLogHandler(stream=sys.stdout))
    logger.propagate = False