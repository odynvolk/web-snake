import random
from time import time


class Proxies(object):
    def __init__(self, filename, reload_time=60*10):
        self.filename = filename
        self.reload_time = reload_time
        self._read()

    def random(self):
        if (self.time + self.reload_time) < time():
            self._read()
        return random.choice(self.proxies)

    def _read(self):
        print 'Reading proxies...'
        with open(self.filename) as f:
            self.proxies = f.read().splitlines()
            self.time = time()
