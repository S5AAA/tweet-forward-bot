#! python3

import sys

class Logger():
    def __init__(self, logfile="bot_log.txt"):
        self.terminal = sys.stdout
        self.log = open(logfile, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def init(self):
        sys.stdout = self

    def finit(self):
        self.log.close()
