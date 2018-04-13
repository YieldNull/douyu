import logging
import os

SERVER_ADDRESS = 'openbarrage.douyutv.com'
SERVER_PORT = 8601

FILE_STORAGE_DATE_FORMAT = '%Y_%m_%d'
FILE_STORAGE_REPOSITORY = '/home/douyu/msg'
FILE_STORAGE_NAME_FORMAT = os.path.join(FILE_STORAGE_REPOSITORY, '{name}_{date}.txt')

COUNTER_PERIOD = 30
INDEXING_PERIOD = 10

LOGGING_LEVEL = logging.DEBUG
LOGGING_BASIC_FORMATTER = '%(asctime)s [%(name)s] %(levelname)s pid-%(process)d : %(message)s'
LOGGING_FILE_NAME = '/home/douyu/log/danmu.log'

MQ_PARSER_ADDRESS = 'localhost'
MQ_PARSER_PORT = 5672
