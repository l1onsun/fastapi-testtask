import logging
import sys

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(logging.Formatter('[%(process)d] %(asctime)s - %(levelname)s - [%(name)s] - %(message)s'))
logger.addHandler(sh)