import time


class BaseModel(object):
    def __init__(self, params=None, context=None):
        super(BaseModel, self).__init__()

    def calculate_intersections(self):
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


from mTR1 import TR1
from mTR2 import TR2
from mTR3 import TR3
from mTR4 import TR4
from mTR5 import TR5
from mTR7 import TR7
from mTR13 import TR13
from mTR213 import TR213
