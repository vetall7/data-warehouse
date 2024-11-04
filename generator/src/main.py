import time
from utils import save_to_csv, save_attendance_to_csv
from config import *
from generator import Generator
from updater import Updater
import concurrent.futures


def save_data(path, data_dict):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(save_to_csv, data, path, file_name) for file_name, data in data_dict.items()]
        concurrent.futures.wait(futures)

data_to_update = dict()

def prepare_data(config_number):
    global data_to_update

    gen_config = get_generate_config(config_number)
    upd_config = get_update_config(config_number)

    generator = Generator(gen_config)
    start_time = time.time()

    data = generator.generate()

    attendance = generator.generate_attendance(data)
    save_attendance_to_csv(attendance, data, f'time{config_number}', 'attendance')

    if upd_config is None:
        data_to_update = data
    else:
        updater = Updater(upd_config)
        updated_data = updater.update(data_to_update)
        # Concatenate data_to_update and updated_data without rewriting keys
        concatenated_data = {
            k: (data.get(k, []) or []) + (updated_data.get(k, []) or [])
            for k in data.keys()
        }
        data = concatenated_data
    
    save_data(f'time{config_number}', data)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time {config_number}: {execution_time:.2f} seconds")


def main():
    for i in GENERATE_CONFIGS.keys():
        prepare_data(config_number=i)


if __name__ == "__main__":
    main()
