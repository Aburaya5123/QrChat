import logging
import sys
from google.cloud.logging.handlers import ContainerEngineHandler

def cloud_logging_settings() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ContainerEngineHandler(stream=sys.stdout))
    logger.propagate = False