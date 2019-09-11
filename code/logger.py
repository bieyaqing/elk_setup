
import logging, json

from configparser import ConfigParser
from datetime import datetime
from os.path import expanduser
from queue import Queue
from socket import gethostbyname
from socket import gethostname
from threading import Event
from threading import Thread

config = ConfigParser()
home = expanduser("~")

config.read(f"{home}/.elk_setup/config.ini")

class Logger(object):

    NOW = datetime.now()
    NOW_DATE_STR = NOW.strftime("%Y-%m-%d")
    CONF_NAME = config["Logging"].get("LOGGINGFILE", "INFO")
    LOG_FILE_PATH = f"{home}/logs/{NOW_DATE_STR}-{CONF_NAME}"
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
    log_stream_queue = Queue()
    log_stop_event = Event()

    def logging_thread_method(log_stream_queue, stop_event):
        while not stop_event.is_set():
            if not log_stream_queue.empty():
                raw_str = log_stream_queue.get()
                raw_obj = json.loads(raw_str)
                level = raw_obj.get("level")
                msg = raw_obj.get("msg")
                args = raw_obj.get("args")
                port = raw_obj.get("port")
                if level == 'info':
                    logger.info(msg, *args, port=port)
                elif level == 'warning':
                    logger.warning(msg, *args, port=port)
                elif level == 'error':
                    logger.error(msg, *args, port=port)
                elif level == 'debug':
                    logger.debug(msg, *args, port=port)
                elif level == 'critical':
                    logger.critical(msg, *args, port=port)
            else:
                sleep(0.01)

    t = Thread(target=logging_thread_method, args=(log_stream_queue, log_stop_event,))
    t.start()

    @staticmethod
    def info(msg, *args, port=None):
        SharedLogger.log_stream_queue.put(json.dumps({
            "level": "info",
            "msg": msg,
            "args": args,
            "port": port
        }))

    @staticmethod
    def warning(msg, *args, port=None):
        SharedLogger.log_stream_queue.put(json.dumps({
            "level": "warning",
            "msg": msg,
            "args": args,
            "port": port
        }))

    @staticmethod
    def error(msg, *args, port=None):
        SharedLogger.log_stream_queue.put(json.dumps({
            "level": "error",
            "msg": msg,
            "args": args,
            "port": port
        }))

    @staticmethod
    def debug(msg, *args, port=None):
        SharedLogger.log_stream_queue.put(json.dumps({
            "level": "debug",
            "msg": msg,
            "args": args,
            "port": port
        }))

    @staticmethod
    def critical(msg, *args, port=None):
        SharedLogger.log_stream_queue.put(json.dumps({
            "level": "critical",
            "msg": msg,
            "args": args,
            "port": port
        }))

        