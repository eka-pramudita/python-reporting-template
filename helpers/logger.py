import logging
import os
import sys
from pythonjsonlogger import jsonlogger


def get_logger(name):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StackdriverJsonFormatter(timestamp=True))
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        #format='%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s',
        handlers=[handler]
    )

    logger = logging.getLogger(name)
    return logger


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):

    def __init__(self, fmt="%(name) %(levelname) %(message)", style='%', *args, **kwargs):
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self, log_record):
        log_record['severity'] = log_record['levelname']
        del log_record['levelname']

        return super(StackdriverJsonFormatter, self).process_log_record(log_record)