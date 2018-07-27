import sys
from .logging import getLogger

logger = getLogger(__name__)


def fail(exit_code=1):
    logger.critical("** FATAL ERROR **")
    sys.exit(exit_code)
