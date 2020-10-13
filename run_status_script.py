from datetime import datetime, timedelta
from os import mkdir, path, remove
import numpy as np
import pandas as pd
import subprocess 
import time
import urllib.request

WIFI_NAME = "ABCD" 

def run_for_day(file_name, total_minutes):
    df = pd.DataFrame(columns=['Timestamp', 'Status'])
    tick_start = time.time()

    for i in range(total_minutes):  
        local_file = open('local_file.txt', 'r')
        line1 = local_file.readline()

        condition_1 = False
        condition_2 = False

        if WIFI_NAME in subprocess.check_output("iwgetid").decode("utf-8"):
            condition_1 = True

            url = "https://raw.githubusercontent.com/nihesh7391/wifi_stats/master/remote_file.txt"
            try:
                urllib.request.urlretrieve(url, 'remote_file.txt')
                condition_2 = path.exists('remote_file.txt')
            except:
                continue

        if (condition_1 and condition_2): 
            remote_file = open('remote_file.txt', 'r')
            line2 = remote_file.readline()
            if (line1==line2):
                cur_time = datetime.now()
                new_row = {'Timestamp': str(cur_time.hour)+':'+str(cur_time.minute), 'Status': '1'}
                df = df.append(new_row, ignore_index=True)
        else:
            cur_time = datetime.now()
            new_row = {'Timestamp': str(cur_time.hour)+':'+str(cur_time.minute), 'Status': '0'}
            df = df.append(new_row, ignore_index=True)
        
        if condition_2:
            remove('remote_file.txt')
        
        time.sleep(60.0 - ((time.time() - tick_start) % 60.0))        

    df.to_csv(file_name, index=False)

if not path.isdir('Records/'):
    mkdir('Records')

while True: 
    ref_time = datetime.now().replace(microsecond=0)
    midnight_time = ref_time.replace(hour = 23, minute = 59, second = 59, microsecond=0)
    time_diff = midnight_time - ref_time
    total_minutes = int(np.floor(time_diff.total_seconds()/60))

    record_name = 'Records/'+ref_time.strftime("%d_%m_%Y")+'.csv'

    run_for_day(record_name, total_minutes)
