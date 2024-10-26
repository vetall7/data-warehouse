import time
from utils import save_to_csv
from config import *
from generator import Generator
import concurrent.futures


def save_data(path, data_dict):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(save_to_csv, data, path, file_name) for file_name, data in data_dict.items()]
        concurrent.futures.wait(futures)


def generate_data(config_number):
    config = get_config_set(config_number)
    generator = Generator(config)
    start_time = time.time()

    data = generator.generate()
    save_data(f'time{config_number}', data)
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time {config_number}: {execution_time:.2f} seconds")


def main():
    for i in CONFIG_SETS.keys():
        generate_data(config_number=i)


if __name__ == "__main__":
    main()
