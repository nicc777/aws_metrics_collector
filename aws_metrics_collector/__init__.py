import pathlib
import os
from datetime import datetime
import logging
import traceback
import inspect


DEBUG = os.getenv('DEBUG', None)
if DEBUG is not None:   # pragma: no cover
    DEBUG = True        # pragma: no cover
else:                   # pragma: no cover
    DEBUG = False       # pragma: no cover


def get_logging_level():
    if DEBUG is True:           # pragma: no cover
        return logging.DEBUG    # pragma: no cover
    else:                       # pragma: no cover
        return logging.INFO     # pragma: no cover


logger = logging.getLogger(__name__)
logger.setLevel(get_logging_level())

# create console handler and set level to debug
#ch = logging.StreamHandler()
log_file_name = '{}{}aws_metrics_collector.log'.format(
    os.getcwd(),
    os.sep
)
ch = logging.FileHandler(filename=log_file_name)
ch.setLevel(get_logging_level())

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def get_utc_timestamp(with_decimal: bool=False):
    epoch = datetime(1970,1,1,0,0,0)
    now = datetime.utcnow()
    timestamp = (now - epoch).total_seconds()
    if with_decimal:
        return timestamp
    return int(timestamp)


def id_caller()->list:
    result = list()
    try:
        caller_stack = inspect.stack()[2]
        result.append(caller_stack[1].split(os.sep)[-1]) # File name
        result.append(caller_stack[2]) # line number
        result.append(caller_stack[3]) # function name
    except: # pragma: no cover
        pass
    return result


class LogWrapper:
    def __init__(self, logger_impl=logger):
        self.logger = logger_impl
        self.debug_flag = DEBUG

    def _format_msg(self, stack_data: list, message: str)->str:
        if message is not None:
            message = '{}'.format(message)
            if len(stack_data) == 3:
                message = '[{}:{}:{}] {}'.format(
                    stack_data[0],
                    stack_data[1],
                    stack_data[2],
                    message
                )
            return message
        return 'NO_INPUT_MESSAGE'

    def enable_debug(self):
        self.logger.setLevel(logging.DEBUG)
        for handler in self.logger.handlers:
            handler.setLevel(logging.DEBUG)
        self.debug_flag = True

    def disable_debug(self):
        self.logger.setLevel(logging.INFO)
        for handler in self.logger.handlers:
            handler.setLevel(logging.INFO)
        self.debug_flag = False

    def info(self, message: str, **kwargs):
        message = self._format_msg(stack_data=id_caller(), message=message)
        self.logger.info(message)

    def debug(self, message: str, **kwargs):
        if self.debug_flag is True:
            message = self._format_msg(stack_data=id_caller(), message=message)
            self.logger.debug(message)

    def warning(self, message: str, **kwargs):
        message = self._format_msg(stack_data=id_caller(), message=message)
        self.logger.warning(message)
    
    def error(self, message: str, **kwargs):
        message = self._format_msg(stack_data=id_caller(), message=message)
        self.logger.error(message)


# EOF
