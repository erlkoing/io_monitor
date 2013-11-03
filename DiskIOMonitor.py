import time
import psutil

class DiskIOData():
    def __init__(self, disk_name):
        self.disk_name = disk_name
        self.timestamps = []
        self.read_count = []
        self.write_count = []
        self.read_bytes = []
        self.write_bytes = []
        self.read_time = []
        self.write_time = []

    def update_io_data(self, disk_io_data, timestamp):
        self.timestamps.append(timestamp)
        self.read_count.append(disk_io_data.read_count)
        self.write_count.append(disk_io_data.write_count)
        self.read_bytes.append(disk_io_data.read_bytes)
        self.write_bytes.append(disk_io_data.write_bytes)
        self.read_time.append(disk_io_data.read_time)
        self.write_time.append(disk_io_data.write_time)

    def print_all_data(self):
        print("Disk name: " + str(self.disk_name))
        print("Timestamps: " + str(self.timestamps))
        print("Read count: " + str(self.read_count))
        print("Write count: " + str(self.write_count))
        print("Read bytes: " + str(self.read_bytes) + "Bytes")
        print("Write bytes: " + str(self.write_bytes) + "Bytes")
        print("Read time: " + str(self.read_time) + "ms")
        print("Write time: " + str(self.write_time) + "ms")

    def print_actual_data(self, pattern="{0:10} {1:15} {2:15} {3:15} {4:15} {5:15} {6:15}"):
        last_index = len(self.timestamps) - 1
        if last_index >= 0:
            print(pattern.format(str(self.disk_name),
                                 str(self.read_count[last_index]),
                                 str(self.write_count[last_index]),
                                 str(self.read_bytes[last_index]),
                                 str(self.write_bytes[last_index]),
                                 str(self.read_time[last_index]),
                                 str(self.write_time[last_index])))

class DiskIOMonitor():
    def __init__(self, interval, count):
        self.interval = interval
        self.count = count
        self.disks = {}
        self.initialize()

    def initialize(self):
        for disk in psutil.disk_io_counters(True).items():
            disk_name = disk[0]
            self.disks[disk_name] = DiskIOData(disk_name)

    def update_disks_io_data(self):
        disks_data = psutil.disk_io_counters(True).items()
        for disk_data in disks_data:
            disk_name = disk_data[0]
            disk_io_data = disk_data[1]
            self.update_disk_io_data(disk_name, disk_io_data)

    def update_disk_io_data(self, disk_name, disk_io_data):
        timestamp = time.time()

        if not self.disks.__contains__(disk_name):
            self.add_new_disk(disk_name)

        self.disks[disk_name].update_io_data(disk_io_data, timestamp)

    def add_new_disk(self, disk_name):
        self.disks[disk_name] = DiskIOData[disk_name]

    def print(self):
        for disk_name, disk in self.disks.items():
            disk.print_all_data()
            print()

    def print_actual_data(self):
        pattern = "{0:10} {1:15} {2:15} {3:15} {4:15} {5:15} {6:15}"
        print(pattern.format("disk_name",
                             "read_count",
                             "write_count",
                             "read_bytes",
                             "write_bytes",
                             "read_time",
                             "write_time"))

        for disk_name, disk in self.disks.items():
            disk.print_actual_data(pattern)
        print()

    def run(self):
        for i in range(self.count):
            ts1 = time.time()
            self.update_disks_io_data()
            self.print_actual_data()
            ts2 = time.time()

            time.sleep(self.compute_sleep_time(ts1, ts2))

    def compute_sleep_time(self, timestamp1, timestamp2):
        latency = timestamp2 - timestamp1
        sleep_time = self.interval - latency
        return sleep_time