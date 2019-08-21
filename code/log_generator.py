
from datetime import datetime
from random import randrange
from socket import gethostbyname
from socket import gethostname
from time import sleep

class LogGenerator:

    def __init__(self):
        now = datetime.now()
        now_date_str = now.strftime("%Y-%m-%d")
        self.ipaddr = gethostbyname(gethostname())
        self.file_name = f"/home/logs/{now_date_str}.log"
        self.levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
        self.ports = [4500, 4501, 4502, 4503]
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

    def write(self):
        f = open(self.file_name, "a")
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
        level = self.randomVal(self.levels)
        port = self.randomVal(self.ports)
        msg = self.randomVal(self.msgs)
        log = f"{level} {timestamp} {self.ipaddr} {port} {msg}\r\n"
        # print(log)
        f.write(log)
        f.close()

if __name__ == "__main__":
    lg = LogGenerator()
    while True:
        lg.write()
        sleep(1)

