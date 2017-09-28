import logging
import sys

MONGODB_URL = 'mongodb://localhost:27017/'
MONGODB_DATABASE = 'danmu'
MONGODB_COLLECTION = 'douyu'

COUNTER_PERIOD = 2
INDEXING_PERIOD = 10

# logging for room
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter('%(asctime)s [%(name)s] %(levelname)s pid-%(process)d room:%(room)8s: %(message)s'))

logger = logging.getLogger('ROOM')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# logging for scheduler
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter('%(asctime)s [%(name)s] %(levelname)s : %(message)s'))

logger = logging.getLogger('Scheduler')
logger.setLevel(logging.INFO)
logger.addHandler(handler)
