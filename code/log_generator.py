
from datetime import datetime
from logger import Logger as logger
from random import randrange
from socket import gethostbyname
from socket import gethostname
from time import sleep

class LogGenerator:

    def __init__(self):
        self.logger = logger()
        # now = datetime.now()
        # now_date_str = now.strftime("%Y-%m-%d")
        # self.ipaddr = gethostbyname(gethostname())
        # self.file_name = f"/home/logs/{now_date_str}.log"
        self.levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
        self.ports = [4500, 4501, 4502, 4503]
        self.methods = ["GET", "POST", "PATCH", "PUT", "DELETE"]
        # self.paths = ["/api/hello", "/api/world"]
        self.client_ips = ["0.0.0.1", "0.0.0.2", "0.0.0.3"]
        self.users = ["alice", "bob", "chris", 'doggy']
        # self.datas = ['{"a":"b","c":"d"}', '{"e":"f","g":"h"}', '{"i":"j","k":"l"}', '{"m":"n","o":"p"}']
        self.msgs = [
            "For a datetime instance d, str(d) is equivalent to d.isoformat(' ').",
            "All arguments are optional. tzinfo may be None, or an instance of a tzinfo subclass.",
            "The latest representable time, time(23, 59, 59, 999999).",
            "Changed in version 3.3: Equality comparisons between naive and aware time instances don't raise TypeError.",
            "For a time t, str(t) is equivalent to t.isoformat().",
            "This is an abstract base class, meaning that this class should not be instantiated directly.",
            "A concrete subclass of tzinfo may need to implement the following methods.",
            "Return the daylight saving time (DST) adjustment, in minutes east of UTC, or None if DST information isn't known.",
            "These methods are called by a datetime or time object, in response to their methods of the same names."
        ]

    def randomVal(self, _list):
        return _list[randrange(len(_list))]

    def log_info(self, port, msg):
        self.logger.info(msg, port=port)

    def log_debug(self, port, msg):
        self.logger.debug(msg, port=port)

    def log_error(self, port, msg):
        self.logger.error(msg, port=port)

    def log_warning(self, port, msg):
        self.logger.warning(msg, port=port)

    def write(self):
        # f = open(self.file_name, "a")
        # now = datetime.now()
        level = self.randomVal(self.levels)
        # timestamp = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
        port = self.randomVal(self.ports)
        method = self.randomVal(self.methods)
        # path = self.randomVal(self.paths)
        client_ip = self.randomVal(self.client_ips)
        username = self.randomVal(self.users)
        # code_path = self.randomVal(self.code_paths)
        # data = self.randomVal(self.datas)
        msg = self.randomVal(self.msgs)
        msg = f"{method} {client_ip} {username} {msg}"
        # log = f"{level} {timestamp} {self.ipaddr} {port} {method} {path} {client_ip} {username} {code_path} {data}\r\n"
        # print(log)
        # f.write(log)
        # f.close()
        if level == "INFO":
            self.log_info(port, msg)
        elif level == "DEBUG":
            self.log_debug(port, msg)
        elif level == "WARNING":
            self.log_warning(port, msg)
        elif level == "ERROR":
            self.log_error(port, msg)

if __name__ == "__main__":
    lg = LogGenerator()
    while True:
        lg.write()
        sleep(0.1)

