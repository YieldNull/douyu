import logging
import sys

SERVER_ADDRESS = 'openbarrage.douyutv.com'
SERVER_PORT = 8601

MONGODB_URL = 'mongodb://localhost:27017/'
MONGODB_DATABASE = 'danmu'
MONGODB_COLLECTION = 'douyu'
MONGODB_PARSE_MSG = False

STORAGE_CLASS = 'MongodbStorage'

COUNTER_PERIOD = 2
INDEXING_PERIOD = 10

LOGGING_LEVEL = logging.INFO
LOGGING_STREAM = sys.stdout
LOGGING_BASIC_FORMATTER = '%(asctime)s [%(name)s] %(levelname)s pid-%(process)d : %(message)s'
