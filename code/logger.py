
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
    FORMAT = "%(_level)s %(asctime)-15s %(_server_ip)s %(_port)s %(_filename)s:%(_function)s:%(_line)d %(message)s"
    logging.basicConfig(filename=LOG_FILE_PATH, filemode="a", format=FORMAT)
    CONF_LEVEL = config["Logging"].get("LOGGINGLEVEL", "INFO")
    LEVEL = logging._nameToLevel[CONF_LEVEL]

    def __init__(self, logger_name=__name__, port="0000"):
        self.logger = logging.getLogger(name=logger_name)
        self.logger.setLevel(Logger.LEVEL)
        self.server_ip = gethostbyname(gethostname())
        self.port = port

    def _prepare_extra(self, filename, line, function, port):
        if filename[0] != "/":
            filename = "/" + filename
        return {
            "_level": "INFO",
            "_filename": filename,
            "_line": line,
            "_function": function,
            "_server_ip": self.server_ip,
            "_port": self.port if port is None else port
        }

    def info(self, msg, *args, port=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.logger.info(msg, *args, extra=self._prepare_extra(_filename, _line, _function, port))
        
    def warning(self, msg, *args, port=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.logger.warning(msg, *args, extra=self._prepare_extra(_filename, _line, _function, port))

    def error(self, msg, *args, port=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.logger.error(msg, *args, extra=self._prepare_extra(_filename, _line, _function, port))

    def debug(self, msg, *args, port=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.logger.debug(msg, *args, extra=self._prepare_extra(_filename, _line, _function, port))

    def critical(self, msg, *args, port=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.logger.critical(msg, *args, extra=self._prepare_extra(_filename, _line, _function, port))

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

        