import logging
import sys
import os

SERVER_ADDRESS = 'openbarrage.douyutv.com'
SERVER_PORT = 8601

STORAGE_CLASS = 'FileStorage'
STORAGE_ASYNC = False

PARSER_CLASS = 'RegexParser'

FILE_STORAGE_REPOSITORY = '/home/junjie/msg'
FILE_STORAGE_DATE_FORMAT = '%Y_%m_%d'
FILE_STORAGE_NAME_FORMAT = FILE_STORAGE_REPOSITORY + '/{name}_{date}.txt'

COUNTER_PERIOD = 30
INDEXING_PERIOD = 10

LOGGING_LEVEL = logging.INFO
LOGGING_STREAM = sys.stdout
LOGGING_BASIC_FORMATTER = '%(asctime)s [%(name)s] %(levelname)s pid-%(process)d : %(message)s'
LOGGING_USE_FILE = True
LOGGING_FILE_NAME = '/home/junjie/log/danmu.log'

MQ_PARSER_ADDRESS = 'localhost'
MQ_PARSER_PORT = 5672

MQ_DISPATCHER_ADDRESS = 'localhost'
MQ_DISPATCHER_PORT = 5672
