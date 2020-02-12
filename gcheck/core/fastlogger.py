# -*- coding: utf-8 -*-
"""

@author: lutianyang
"""
__VERSION__ = 1.0

import os
import logging
import socket
from logging.handlers import TimedRotatingFileHandler as TimedRotatingFileHandlerBase

DEFAULT_FILENAME = 'run.log'
DEFAULT_LOGDIR = '_log_'

DEFAULT_FORMAT = '%(asctime)s [%(levelname)-8s] %(module)11s:%(lineno)-4d - %(message)s'

DEFAULT_FORMAT_COLOR = '%(asctime)s [%(levelname)-8s] %(hostname)s %(module)15s:%(lineno)-4d %(message)s'

DEFAULT_FILECHARPAGE = 'UTF-8'

DEFAULT_FIELD_STYLES = dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color='white', ),
    programname=dict(color='cyan'),
    name=dict(color='blue'))


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


class TimedRotatingFileHandler(TimedRotatingFileHandlerBase):
    pass


@singleton
class _LoggerController(object):

    def __init__(self, saved_dir, saved_filename):
        self.save_dir = saved_dir
        self.save_filename = saved_filename
        self._exist_logger = dict()

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        self._full_path = os.path.join(self.save_dir, self.save_filename)

    def getlogger(self, name: str) -> logging.Logger:
        """
        Fastly generate a logger which contains log to Console and File named `{hostname}.log`.

        Parameters
        ----
        name: str
            the sigunature to retrieve logger.
        logfname: str
            the filename which log infomation will be written to,
            DEFAULT_FILENAME:run.log.

        Examples
        --------

        >>> lo=getloggerfast(__name__)
        >>> lo.debug('debug message') # info also dump to file `run.log`
        2017-10-04 04:05:14,375 - __main__ - INFO     - info message

        """

        if name in self._exist_logger.keys():
            return self._exist_logger[name]
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter(DEFAULT_FORMAT)

        fth = TimedRotatingFileHandler(
            filename=self._full_path, delay=True, when='MIDNIGHT', backupCount=10)
        fth.setFormatter(formatter)
        logger.addHandler(fth)

        self._exist_logger[name] = logger
        return logger


logfilename = '{}.log'.format(socket.gethostname())
_loggercontroller = _LoggerController(DEFAULT_LOGDIR, logfilename)


def getloggerfast(hisname: object) -> object:
    """
    Fetch a logger.Normally, the application just need one logger instance.

    :param hisname: not used for one application
    :return:
    """
    hisname = 'default_holder'
    return _loggercontroller.getlogger(hisname)


if __name__ == '__main__':
    lo = getloggerfast(__name__)

    lo.debug('debug message')
    lo.info('info message')
    lo.warning('warn message')
    lo.error('error message')
    lo.critical('critical message')