import logging

LOGGING_LEVEL = logging.DEBUG

logging.basicConfig(
    level=LOGGING_LEVEL, format="[%(levelname)s] %(asctime)s %(name)s : %(message)s"
)

logger = logging.getLogger(__name__)
