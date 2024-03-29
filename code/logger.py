import json
import logging

from configparser import ConfigParser
# from datetime import datetime
from logging.handlers import RotatingFileHandler
from os.path import expanduser
from queue import Queue
from socket import gethostbyname
from socket import gethostname
from threading import Event
from threading import Thread
from time import sleep

config = ConfigParser()
home = expanduser("~")

config.read(f"{home}/.elk_setup/config.ini")


class Logger(object):

    # NOW = datetime.now()
    # NOW_DATE_STR = NOW.strftime("%Y-%m-%d")
    FORMAT = "%(levelname)s %(asctime)-15s %(_server_ip)s %(_port)s %(_filename)s:%(_function)s:%(_line)d %(message)s"
    
    LOGGINGFILE = config["Logging"].get("LOGGINGFILE", "default.log")
    LOGGINGLEVEL = config["Logging"].get("LOGGINGLEVEL", "INFO")

    # LOG_PATH = f"{home}/logs/{NOW_DATE_STR}-{LOGGINGFILE}"
    LOG_PATH = f"{home}/logs/{LOGGINGFILE}"
    LOG_LEVEL = logging._nameToLevel[LOGGINGLEVEL]

    def __init__(self, logger_name=__name__, log_path=LOG_PATH, port="0000"):
        self.logger = logging.getLogger(name=logger_name)
        self.logger.setLevel(Logger.LOG_LEVEL)
        if self.logger.hasHandlers():
            for hdl in self.logger.handlers:
                self.logger.removeHandler(hdl)
        handler = RotatingFileHandler(log_path, maxBytes=50 * 1024 * 1024, backupCount=100, encoding="UTF-8")
        handler.setFormatter(logging.Formatter(Logger.FORMAT))
        self.logger.addHandler(handler)
        self.server_ip = gethostbyname(gethostname())
        self.port = port
        self.log_stream_queue = Queue()
        self.log_stop_event = Event()
        self.t = Thread(target=self.logging_thread_method, args=(self.log_stream_queue, self.log_stop_event,))
        self.t.setDaemon(True)
        self.t.start()

    def stop(self):
        self.log_stop_event.set()
        self.t.join()

    def logging_thread_method(self, log_stream_queue, log_stop_event):
        while not log_stop_event.is_set():
            if not log_stream_queue.empty():
                raw_str = log_stream_queue.get()
                raw_obj = json.loads(raw_str)
                level = raw_obj.get("level")
                msg = raw_obj.get("msg")
                args = raw_obj.get("args")
                extra = raw_obj.get("extra")
                if level == "info":
                    self.logger.info(msg, *args, extra=extra)
                elif level == "warning":
                    self.logger.warning(msg, *args, extra=extra)
                elif level == "error":
                    self.logger.error(msg, *args, extra=extra)
                elif level == "debug":
                    self.logger.debug(msg, *args, extra=extra)
                elif level == "critical":
                    self.logger.critical(msg, *args, extra=extra)
            else:
                sleep(0.01)

    def _prepare_extra(self, filename, line, function, port):
        if filename[0] != "/":
            filename = "/" + filename
        return {
            "_filename": filename,
            "_line": line,
            "_function": function,
            "_server_ip": self.server_ip,
            "_port": self.port if port is None else port
        }

    def _prepare_queue_obj(self, level, msg, *args, extra):
        return json.dumps({
            "level": level,
            "msg": msg,
            "args": args,
            "extra": extra
        })

    def info(self, msg, *args, port=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.log_stream_queue.put(self._prepare_queue_obj("info", msg, *args, extra=self._prepare_extra(_filename, _line, _function, port)))

    def warning(self, msg, *args, port=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.log_stream_queue.put(self._prepare_queue_obj("warning", msg, *args, extra=self._prepare_extra(_filename, _line, _function, port)))

    def error(self, msg, *args, port=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.log_stream_queue.put(self._prepare_queue_obj("error", msg, *args, extra=self._prepare_extra(_filename, _line, _function, port)))

    def debug(self, msg, *args, port=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.log_stream_queue.put(self._prepare_queue_obj("debug", msg, *args, extra=self._prepare_extra(_filename, _line, _function, port)))

    def critical(self, msg, *args, port=None):
        _filename, _line, _function, _stack = self.logger.findCaller(stack_info=True)
        self.log_stream_queue.put(self._prepare_queue_obj("critical", msg, *args, extra=self._prepare_extra(_filename, _line, _function, port)))
