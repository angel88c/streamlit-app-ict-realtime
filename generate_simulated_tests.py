import time
import os
import random
import shutil
from pathlib import Path
from hreader_module.hreader import *
from csv import DictWriter

FORMAT_FILE = r'.\BASE'
OUTPUT_FILE     = r"\\192.168.0.23\shared\IBTEST_BCM901"
ROOT_FOLDER_CSV = r"\\192.168.0.23\shared\IBTEST_BCM901\CSV"

def get_time_str():
    return time.strftime("%y%m%d%H%M%S")

def replace_in_file(new_file, pattern, value):
    
    with open(new_file) as file:
        content = file.read()
        content = content.replace(pattern, value)
    
    with open(new_file, 'w') as file:
        file.write(content)


def update_files(tests):
    for test in tests:
        #print (test.keys())
        file_path = Path(os.path.join(ROOT_FOLDER_CSV, f"{test['name']}.csv"))
        file_path.touch(exist_ok=True)
        
        with open(file_path, mode="a") as file:
            writer = DictWriter(file, fieldnames=test.keys())
            if file.tell() == 0:
                writer.writeheader()
            
            writer.writerow(test)
            file.close()    


if __name__ == '__main__':

    serial_numbers = ["KBH000001", "KBH000002", "KBH000003", "KBH000004", "KBH000005", "KBH000006"]

    for serial_number in serial_numbers:
        new_file = f'{FORMAT_FILE}_{serial_number}'
        new_file = os.path.join(OUTPUT_FILE, new_file)
        shutil.copyfile(FORMAT_FILE, new_file)

        replace_in_file(new_file, r"%START_TIME%", get_time_str())
        replace_in_file(new_file, r"%SERIAL_NUMBER%", serial_number)
        
        for i in range(1, 11):
            print(f"Testing {i}")
            value = f'{random.uniform(1.2E-07, 8.7E-08):.5e}'             
            replace_in_file(new_file, f"%VALUE_{i:02d}%", value)
            time.sleep(.2)

        print(f"Testing 11")
        value_1 = f'{random.uniform(+2E-01, 0):.5e}'
        replace_in_file(new_file, f"%VALUE_11%", value_1)
        time.sleep(.2)
        
        print(f"Testing 12")
        value_2 = f'{random.uniform(+3.6, +2.95,):.5e}'
        replace_in_file(new_file, f"%VALUE_12%", value_2)
        time.sleep(.2)
        
        replace_in_file(new_file, r"%PRJ%", "IBTEST_BCM901")
        replace_in_file(new_file, r"%END_TIME%", get_time_str())
        
        tests = get_all_tests(new_file)
        update_files(tests)