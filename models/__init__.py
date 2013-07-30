import time


class BaseModel(object):
    def __init__(self, params=None, context=None):
        super(BaseModel, self).__init__()

    def create_equations(self):
        pass

    def solve(self):
        pass

    def start(self):
        self.t1 = time.time()

    def stop(self):
        self.t2 = time.time()
        timedif = self.t2 - self.t1
        print timedif, ' seconds'

    def get_volume(self):
        pass


from TR1 import *
from TR2 import *
from TR3 import *
from TR7 import *
from TR13 import *
from TR20 import *