import time
import subprocess
import re

class TimeData():
    def __init__(self,data):
        self.file_names = [item[8] for item in data]
        self.pids = [item[1] for item in data]
        self.prognames = [item[0] for item in data]
        self.write_reads = [item[3][-1] for item in data]

class FilesIOData():
    def __init__(self):
        self.timestamps = []
        self.time_datas = []

    def update_files_data(self, time_data, timestamp):
        self.timestamps.append(timestamp)
        self.time_datas.append(time_data)

    def print_actual_data(self, pattern="{0:15} {1:15} {2:15}"):
        last_index = len(self.timestamps) - 1
        if last_index >= 0:
            for i in range (0, len(self.time_datas[last_index].file_names)):
                print(pattern.format(
                                     str(self.time_datas[last_index].file_names[i]),
                                     str(self.time_datas[last_index].prognames[i]),
                                     str(self.time_datas[last_index].write_reads[i])))

class FilesIOMonitor():
    def __init__(self, interval, count):
        self.interval = interval
        self.count = count
        self.initialize()
        self.data

    def initialize(self):
        self.data = FilesIOData()

    def print(self):
        for disk_name, disk in self.disks.items():
            disk.print_all_data()
            print()

    def print_actual_data(self):
        pattern = "{0:15} {1:15} {2:15}"
        print(time.strftime("%a, %d %b %Y %H:%M:%S +0000", self.data.timestamps[-1]))
        print(pattern.format("disk_name",
                             "read_count",
                             "write_count"))

        self.data.print_actual_data(pattern)
        print()
    
    def get_data(self):
        lsof = subprocess.getoutput('lsof | grep REG')
        lines = lsof.split('\n')
        table = [re.split("\s+",line) for line in lines]
        fds = list(filter(lambda x: x[3][0].isdigit(), table))
        return fds

    def run(self):
        for i in range(self.count):
            ts1 = time.time()
            self.data.update_files_data(TimeData(self.get_data()),time.localtime())
            self.print_actual_data()
            ts2 = time.time()

            time.sleep(self.compute_sleep_time(ts1, ts2))

    def compute_sleep_time(self, timestamp1, timestamp2):
        latency = timestamp2 - timestamp1
        sleep_time = self.interval - latency
        return sleep_time

FilesIOMonitor(2,5).run()