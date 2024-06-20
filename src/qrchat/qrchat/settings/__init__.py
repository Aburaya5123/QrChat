import os

if os.getenv("REMOTE_DEPLOY", False):
    from .deployment import *
    from ..logging_controler import cloud_logging_settings
    cloud_logging_settings()
else:
    from .local import *