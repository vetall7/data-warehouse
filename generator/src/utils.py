import os
import random
import pandas as pd

class Range:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def random(self):
        return random.randint(self.min, self.max)


def save_to_csv(data, file_name):
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    data_df = pd.DataFrame([vars(o) for o in data])
    save_path = os.path.join(data_dir, f'{file_name}.csv')

    data_df.to_csv(save_path, index=False)
    