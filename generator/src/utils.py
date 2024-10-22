import random
import faker

class Range:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def random(self):
        return random.randint(self.min, self.max)
