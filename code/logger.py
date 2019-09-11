
import logging

from configparser import ConfigParser
from datetime import datetime
from os.path import expanduser
from socket import gethostbyname
from socket import gethostname

config = ConfigParser()
home = expanduser("~")

config.read(f"{home}/.elk_setup/config.ini")

class Logger(object):

    NOW = datetime.now()
    NOW_DATE_STR = NOW.strftime("%Y-%m-%d")
    LOG_FILE_PATH = f"{home}/logs/{NOW_DATE_STR}.log"
    FORMAT = "%(_level)s %(asctime)-15s %(_server_ip)s %(_port)s %(_method)s %(_path)s %(_client_ip)s %(_username)s %(_filename)s:%(_function)s:%(_line)d %(message)s"
    logging.basicConfig(filename=LOG_FILE_PATH, filemode="a", format=FORMAT)
    CONF_LEVEL = config["Logging"].get("LOGGINGLEVEL", "INFO")
    if CONF_LEVEL == "INFO":
        LEVEL = logging.INFO
    elif CONF_LEVEL == "DEBUG":
        LEVEL = logging.DEBUG
    else:
        LEVEL = logging.INFO

    def __init__(self, logger_name=__name__, port="0000", client_ip="0.0.0.0", username="incognito"):
        self.logger = logging.getLogger(name=logger_name)
        self.logger.setLevel(Logger.LEVEL)
        self.server_ip = gethostbyname(gethostname())
        self.port = port
        self.client_ip = client_ip
        self.username = username

    def info(self, msg, *args, port=None, client_ip=None, username=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.logger.info(msg, *args, extra={
            "_level": "INFO",
            "_filename": _filename,
            "_line": _line,
            "_function": _function,
            "_server_ip": self.server_ip,
            "_port": self.port if port is None else port,
            "_method": _function,
            "_path": _filename,
            "_client_ip": self.client_ip if client_ip is None else client_ip,
            "_username": self.username if username is None else username
        })
        
    def warning(self, msg, *args, port=None, client_ip=None, username=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.logger.warning(msg, *args, extra={
            "_level": "WARNING",
            "_filename": _filename,
            "_line": _line,
            "_function": _function,
            "_server_ip": self.server_ip,
            "_port": self.port if port is None else port,
            "_method": _function,
            "_path": _filename,
            "_client_ip": self.client_ip if client_ip is None else client_ip,
            "_username": self.username if username is None else username
        })

    def error(self, msg, *args, port=None, client_ip=None, username=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.logger.error(msg, *args, extra={
            "_level": "ERROR",
            "_filename": _filename,
            "_line": _line,
            "_function": _function,
            "_server_ip": self.server_ip,
            "_port": self.port if port is None else port,
            "_method": _function,
            "_path": _filename,
            "_client_ip": self.client_ip if client_ip is None else client_ip,
            "_username": self.username if username is None else username
        })

    def debug(self, msg, *args, port=None, client_ip=None, username=None):
        logger = logging.getLogger(name="debug")
        logger.setLevel(Logger.LEVEL)
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.logger.debug(msg, *args, extra={
            "_level": "DEBUG",
            "_filename": _filename,
            "_line": _line,
            "_function": _function,
            "_server_ip": self.server_ip,
            "_port": self.port if port is None else port,
            "_method": _function,
            "_path": _filename,
            "_client_ip": self.client_ip if client_ip is None else client_ip,
            "_username": self.username if username is None else username
        })

class SharedLogger(object):

    logger = Logger("SHARED")

    @staticmethod
    def info(msg, *args, port=None, client_ip=None, username=None):
        SharedLogger.logger.info(msg, *args, port=port, client_ip=client_ip, username=username)

    @staticmethod
    def warning(msg, *args, port=None, client_ip=None, username=None):
        SharedLogger.logger.warning(msg, *args, port=port, client_ip=client_ip, username=username)

    @staticmethod
    def error(msg, *args, port=None, client_ip=None, username=None):
        SharedLogger.logger.error(msg, *args, port=port, client_ip=client_ip, username=username)

    @staticmethod
    def debug(msg, *args, port=None, client_ip=None, username=None):
        SharedLogger.logger.debug(msg, *args, port=port, client_ip=client_ip, username=username)

        