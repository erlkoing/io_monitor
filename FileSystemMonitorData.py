#!/usr/bin/env python

import numpy

class FileSystemMonitorData:
    def __init__(self, filename1, filename2):
        self.proc_data_list = list()
        self.part_data_list = list()
        self.file_data_list = list()
        self.parse_proc(filename1)
        self.parse_part(filename2)

    def get_proc_data_list(self):
        return self.proc_data_list

    def get_part_data_list(self):
        return self.part_data_list

    def parse_proc(self, filename):
        file = open(filename,'r') 
        lines = file.readlines()

        for line in lines:
            if not line.startswith('\n') and not line.startswith("pid"):
                info = line.split()

                pid = info[0]
                name = info[1]
                ex = None
                for pd in self.proc_data_list:
                    if (pd.get_pid() == pid) and (pd.get_name() == name):
                        ex = pd

                if ex == None:
                    ex = ProcessData(pid, name)
                    self.proc_data_list.append(ex)

                ex.add_entry(info[2], info[4], info[3], info[5])

        file.close()
        pass

    def parse_part(self, filename):
        file = open(filename,'r') 
        lines = file.readlines()

        for line in lines:
            if not line.startswith('\n') and not line.startswith("disk_name"):
                info = line.split()

                name = info[0]
                ex = None
                for pd in self.part_data_list:
                    if pd.get_name() == name:
                        ex = pd

                if ex == None:
                    ex = PartitionData(name)
                    self.part_data_list.append(ex)

                ex.add_entry(info[1], info[3], info[5], info[2], info[4], info[6])

        file.close()
        pass

class ProcessData:
    def __init__(self, pid, name):
        self.pid = pid
        self.name = name

        self.read_count = list()
        self.write_count = list()
        self.read_write_count = list()

        self.read_bytes = list()
        self.write_bytes = list()
        self.read_write_bytes = list()

    def get_pid(self):
        return self.pid

    def get_name(self):
        return self.name

    def get_frequency(self, counter):
        if counter == 'r':
            return self.read_count[0]
        else:
            if counter == 'w':
                return self.write_count[0]
            else:
                return self.read_write_count[0]

    def get_dataflow(self, counter):
        if counter == 'r':
            return self.read_bytes[0]
        else:
            if counter == 'w':
                return self.write_bytes[0]
            else:
                return self.read_write_bytes[0]

    def get_read_count(self):
        return self.read_count

    def get_write_count(self):
        return self.write_count

    def get_read_write_count(self):
        return self.read_write_count

    def get_read_bytes(self):
        return self.read_bytes

    def get_write_bytes(self):
        return self.write_bytes

    def get_read_write_bytes(self):
        return self.read_write_bytes

    def add_entry(self, r_count, r_bytes, w_count, w_bytes):
        self.read_count.append(r_count)
        self.write_count.append(w_count)
        self.read_write_count.append(int(r_count)+int(w_count))

        self.read_bytes.append(r_bytes)
        self.write_bytes.append(w_bytes)
        self.read_write_bytes.append(int(r_bytes)+int(w_bytes))

class PartitionData:
    def __init__(self, name):
        self.name = name

        self.read_count = list()
        self.write_count = list()
        self.read_write_count = list()

        self.read_bytes = list()
        self.write_bytes = list()
        self.read_write_bytes = list()

        self.read_time = list()
        self.write_time = list()
        self.read_write_time = list()

    def get_name(self):
        return self.name

    def get_frequency(self, counter):
        if counter == 'r':
            return self.read_count[0]
        else:
            if counter == 'w':
                return self.write_count[0]
            else:
                return self.read_write_count[0]

    def get_dataflow(self, counter):
        if counter == 'r':
            return self.read_bytes[0]
        else:
            if counter == 'w':
                return self.write_bytes[0]
            else:
                return self.read_write_bytes[0]

    def get_time(self, counter):
        if counter == 'r':
            return self.read_time[0]
        else:
            if counter == 'w':
                return self.write_time[0]
            else:
                return self.read_write_time[0]

    def get_read_count(self):
        return self.read_count

    def get_write_count(self):
        return self.write_count

    def get_read_write_count(self):
        return self.read_write_count

    def get_read_bytes(self):
        return self.read_bytes

    def get_write_bytes(self):
        return self.write_bytes

    def get_read_write_bytes(self):
        return self.read_write_bytes

    def get_read_time(self):
        return self.read_time

    def get_write_time(self):
        return self.write_time

    def get_read_write_time(self):
        return self.read_write_time

    def add_entry(self, r_count, r_bytes, r_time, w_count, w_bytes, w_time):
        self.read_count.append(r_count)
        self.write_count.append(w_count)
        self.read_write_count.append(int(r_count)+int(w_count))

        self.read_bytes.append(r_bytes)
        self.write_bytes.append(w_bytes)
        self.read_write_bytes.append(int(r_bytes)+int(w_bytes))

        self.read_time.append(r_time)
        self.write_time.append(w_time)
        self.read_write_time.append(int(r_time)+int(w_time))

