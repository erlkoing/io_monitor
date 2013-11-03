import time
import psutil

class ProcessIOData():

    def __init__(self, process_info):
        self.pid = process_info.pid
        self.name = process_info.name
        self.create_time = process_info.create_time
        self.timestamps = []
        self.read_count = []
        self.write_count = []
        self.read_bytes = []
        self.write_bytes = []

    def update_io_data(self, process_io_data, timestamp):
        self.timestamps.append(timestamp)
        self.read_count.append(process_io_data.read_count)
        self.write_count.append(process_io_data.write_count)
        self.read_bytes.append(process_io_data.read_bytes)
        self.write_bytes.append(process_io_data.write_bytes)

    def print_all_data(self):
        print("PID: " + str(self.pid))
        print("Process name: " + str(self.name))
        print("Create time: " + str(self.create_time))
        print("Timestamps: " + str(self.timestamps))
        print("Read counts: " + str(self.read_count))
        print("Write counts: " + str(self.write_count))
        print("Read bytes: " + str(self.read_bytes))
        print("Write bytes: " + str(self.write_bytes))

    def print_actual_data(self, pattern="{0:12} {1:10} {2:10} {3:10} {4:10} {5:10}"):
        last_index = len(self.timestamps) - 1
        if last_index >= 0:
            print(pattern.format(str(self.pid),
                                 str(self.name),
                                 str(self.read_count[last_index]),
                                 str(self.write_count[last_index]),
                                 str(self.read_bytes[last_index]),
                                 str(self.write_bytes[last_index])))

class ProcessIOMonitor():

    def __init__(self, interval, count):
        self.interval = interval
        self.count = count
        self.processes = {}
        self.initialize()

    def initialize(self):
        for process in psutil.process_iter():
            self.processes[process.pid] = ProcessIOData(process)

    def update_processes_io_data(self):
        for process in psutil.process_iter():
            self.update_process_io_data(process.pid)

    def update_process_io_data(self, pid):
        if not self.processes.__contains__(pid):
            self.add_new_process(pid)

        try:
            process = psutil.Process(pid)
            process_io_data = process.get_io_counters()
            timestamp = time.time()
            self.processes[pid].update_io_data(process_io_data, timestamp)
        except psutil.error.AccessDenied: # gdy odpalamy z poziomu zwyklego uzytkownika sypie wyjatkami przy dostepnie do procesow nie nalezacych du uzytkownika
            pass
            #print("Don't have permission to access " + str(pid) + " I/O data.")

    def print(self):
        for pid, process in self.processes.items():
            process.print_all_data()
            print()

    def print_actual_data(self):
        pattern = "{0:10} {1:40} {2:15} {3:15} {4:15} {5:15}"
        print(pattern.format("pid",
                             "process_name",
                             "read_count",
                             "write_count",
                             "read_bytes",
                             "write_bytes"))

        for pid, process in self.processes.items():
            process.print_actual_data(pattern)
        print()

    def add_new_process(self, pid):
        process = psutil.Process(pid)
        self.processes[pid] = ProcessIOData(process)

    def run(self):
        for i in range(self.count):
            ts1 = time.time()
            self.update_processes_io_data()
            self.print_actual_data()
            ts2 = time.time()

            time.sleep(self.compute_sleep_time(ts1, ts2))

    def compute_sleep_time(self, timestamp1, timestamp2):
        latency = timestamp2 - timestamp1
        sleep_time = self.interval - latency
        return sleep_time