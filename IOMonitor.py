import argparse
from ProcesIOMonitor import ProcessIOMonitor
from DiskIOMonitor import DiskIOMonitor

class IOMonitor():
    def __init__(self):
        self.arguments = None
        self.monitor_type = None
        self.interval = None
        self.iterations = None
        self.parse_arguments()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="IO monitor")

        parser.add_argument("-d", "--delay", help="Delay time interval. Specifies the delay between screen updates.", action="store", type=int, default=1)
        parser.add_argument("-i", "--iterations", help="Number of iterations. Specifies the maximum number of iterations.", action="store", type=int, default=10)
        parser.add_argument("monitor_type", choices=['process', 'disk', 'files'])

        self.arguments = parser.parse_args()
        self.assign_arguments()

    def assign_arguments(self):
        self.monitor_type = self.arguments.monitor_type
        self.interval = self.arguments.delay
        self.iterations = self.arguments.iterations

    def run(self):
        monitor = None
        if self.monitor_type == "disk":
            monitor = DiskIOMonitor(self.interval, self.iterations)
        elif self.monitor_type == "files":
            monitor = FilesIOMonitor(self.interval, self.iterations)
        else:
            monitor = ProcessIOMonitor(self.interval, self.iterations)

        monitor.run()

io_monitor = IOMonitor()
io_monitor.run()

