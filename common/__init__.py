import logging
import sys


def get_logger(name, level=logging.INFO, file_name=None, sep_warning=False,
               format_str='%(asctime)s [%(name)s] %(levelname)s pid-%(process)d : %(message)s'):
    logger = logging.getLogger(name)

    if len(logger.handlers) == 0:
        if not file_name:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter(format_str))

            logger.addHandler(handler)
            logger.setLevel(level)
        else:
            handler = logging.FileHandler(file_name)
            handler.setFormatter(logging.Formatter(format_str))
            handler.setLevel(level)

            logger.addHandler(handler)
            logger.setLevel(level)

            if sep_warning:
                handler = logging.FileHandler('%s_WARNING.log' % file_name)
                handler.setFormatter(logging.Formatter(format_str))
                handler.setLevel(logging.WARNING)

                logger.addHandler(handler)

    return logger
