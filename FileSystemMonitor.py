#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from FileSystemMonitorData import *

class MainWindow:
    def delete(self, widget, event=None):
        gtk.main_quit()
        return False

    def collect_data(self):
        self.all_data = FileSystemMonitorData("proc2.txt", "part2.txt")

    def __init__(self):
        self.collect_data()

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("File System Monitor")
        window.connect("delete_event", self.delete)
        window.set_size_request(800, 500)
        window.set_border_width(10)

        # Create a new notebook, place the position of the tabs
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        window.add(notebook)

        # ========== Append page for processes ==========
        table = gtk.Table(3, 6, False)
        table.set_border_width(10)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        # Creating and filling Tree Store
        self.proc_treestore = gtk.TreeStore(str, str, str)
        self.reload_proc_treestore(None, ['freq', 'r'])
        
        # Creating Tree View
        treeview = gtk.TreeView(self.proc_treestore)
        treeview.set_border_width(10)
        cell = gtk.CellRendererText()

        # Adding columns
        tvcolumn = gtk.TreeViewColumn('Name')
        treeview.append_column(tvcolumn)
        tvcolumn.set_sort_column_id(0)
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 0)

        tvcolumn = gtk.TreeViewColumn('Files')
        treeview.append_column(tvcolumn)
        tvcolumn.set_sort_column_id(1)
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 1)

        tvcolumn = gtk.TreeViewColumn('Metrics')
        treeview.append_column(tvcolumn)
        tvcolumn.set_sort_column_id(2)
		# TODO tvcolumn.set_sort_type
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 2)

        scrolled_window.add_with_viewport(treeview)
        table.attach(scrolled_window, 0, 5, 0, 3)
        treeview.show()
        scrolled_window.show()

        # Creating frame for settings
        frame = gtk.Frame('Settings')
        frame.set_border_width(10)

        vbox = gtk.VBox(False, 5)
        frame.add(vbox)

        # Menu for metrics
        label = gtk.Label('Show:')
        vbox.pack_start(label, False, False, 5)
        label.show()

        button = gtk.RadioButton(None, "frequency")
        button.connect("toggled", self.reload_proc_treestore, ['freq', None])
        button.set_active(True)
        vbox.pack_start(button, False, False, 0)
        button.show()

        button = gtk.RadioButton(button, "dataflow volume")
        button.connect("toggled", self.reload_proc_treestore, ['datafl', None])
        vbox.pack_start(button, False, False, 0)
        button.show()

        label = gtk.Label(' ')
        vbox.pack_start(label, False, False, 0)
        label.show()
        
        # Menu for data type
        label = gtk.Label('Include counters:')
        vbox.pack_start(label, False, False, 5)
        label.show()

        button = gtk.RadioButton(None, "read")
        button.connect("toggled", self.reload_proc_treestore, [None, 'r'])
        button.set_active(True)
        vbox.pack_start(button, False, False, 0)
        button.show()

        button = gtk.RadioButton(button, "write")
        button.connect("toggled", self.reload_proc_treestore, [None, 'w'])
        vbox.pack_start(button, False, False, 0)
        button.show()

        button = gtk.RadioButton(button, "read + write")
        button.connect("toggled", self.reload_proc_treestore, [None, 'r+w'])
        vbox.pack_start(button, False, False, 0)
        button.show()

        vbox.show()
        table.attach(frame, 5, 6, 0, 3)
        frame.show()
        table.show()

        label = gtk.Label('Processes')
        notebook.append_page(table, label)

        # ========== Append page for partitions ==========
        table = gtk.Table(3, 6, False)
        table.set_border_width(10)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        # Creating and filling Tree Store
        self.part_treestore = gtk.TreeStore(str, str, str)
        self.reload_part_treestore(None, ['freq', 'r'])

        # Creating Tree View
        treeview = gtk.TreeView(self.part_treestore)
        treeview.set_border_width(10)
        cell = gtk.CellRendererText()

        # Adding columns
        tvcolumn = gtk.TreeViewColumn('Name')
        treeview.append_column(tvcolumn)
        tvcolumn.set_sort_column_id(0)
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 0)

        tvcolumn = gtk.TreeViewColumn('Files')
        treeview.append_column(tvcolumn)
        tvcolumn.set_sort_column_id(1)
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 1)

        tvcolumn = gtk.TreeViewColumn('Metrics')
        treeview.append_column(tvcolumn)
        tvcolumn.set_sort_column_id(2)
		# TODO tvcolumn.set_sort_type
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 2)

        scrolled_window.add_with_viewport(treeview)
        table.attach(scrolled_window, 0, 5, 0, 3)
        treeview.show()
        scrolled_window.show()

        # Creating frame for settings
        frame = gtk.Frame('Settings')
        frame.set_border_width(10)

        vbox = gtk.VBox(False, 5)
        frame.add(vbox)

        # Menu for metrics
        label = gtk.Label('Show:')
        vbox.pack_start(label, False, False, 5)
        label.show()

        button = gtk.RadioButton(None, "frequency")
        button.connect("toggled", self.reload_part_treestore, ['freq', None])
        button.set_active(True)
        vbox.pack_start(button, False, False, 0)
        button.show()

        button = gtk.RadioButton(button, "dataflow volume")
        button.connect("toggled", self.reload_part_treestore, ['datafl', None])
        vbox.pack_start(button, False, False, 0)
        button.show()

        button = gtk.RadioButton(button, "time")
        button.connect("toggled", self.reload_part_treestore, ['time', None])
        vbox.pack_start(button, False, False, 0)
        button.show()

        label = gtk.Label(' ')
        vbox.pack_start(label, False, False, 0)
        label.show()
        
        # Menu for data type
        label = gtk.Label('Include counters:')
        vbox.pack_start(label, False, False, 5)
        label.show()

        button = gtk.RadioButton(None, "read")
        button.connect("toggled", self.reload_part_treestore, [None, 'r'])
        button.set_active(True)
        vbox.pack_start(button, False, False, 0)
        button.show()

        button = gtk.RadioButton(button, "write")
        button.connect("toggled", self.reload_part_treestore, [None, 'w'])
        vbox.pack_start(button, False, False, 0)
        button.show()

        button = gtk.RadioButton(button, "read + write")
        button.connect("toggled", self.reload_part_treestore, [None, 'r+w'])
        vbox.pack_start(button, False, False, 0)
        button.show()

        vbox.show()
        table.attach(frame, 5, 6, 0, 3)
        frame.show()
        table.show()

        label = gtk.Label('Partitions')
        notebook.append_page(table, label)

        # ========== Append page for files ==========
        table = gtk.Table(3, 6, False)
        table.set_border_width(10)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        # Creating and filling Tree Store
        treestore = gtk.TreeStore(str, str, int)
        for parent in range(4):
            pointer = treestore.append(None, [('parent %i' % parent), '4 files', 12345])
            for child in range(3):
                treestore.append(pointer, [('child %i of parent %i' % (child, parent)), '3 files', 321])

        # Creating Tree View
        treeview = gtk.TreeView(treestore)
        treeview.set_border_width(10)
        treeview.set_headers_visible(False)
        cell = gtk.CellRendererText()

        # Adding columns
        tvcolumn = gtk.TreeViewColumn('Name')
        treeview.append_column(tvcolumn)
        tvcolumn.set_sort_column_id(0)
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 0)

        tvcolumn = gtk.TreeViewColumn('Files')
        treeview.append_column(tvcolumn)
        tvcolumn.set_sort_column_id(1)
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 1)

        tvcolumn = gtk.TreeViewColumn('Frequency')
        treeview.append_column(tvcolumn)
        tvcolumn.set_sort_column_id(2)
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 2)

        scrolled_window.add_with_viewport(treeview)
        table.attach(scrolled_window, 0, 5, 0, 3)
        treeview.show()
        scrolled_window.show()

        # Creating frame for settings
        frame = gtk.Frame('Settings')
        frame.set_border_width(10)

        vbox = gtk.VBox(False, 5)
        frame.add(vbox)

        # Menu for metrics
        label = gtk.Label('Show:')
        vbox.pack_start(label, False, False, 5)
        label.show()

        button = gtk.RadioButton(None, "frequency")
        button.connect("toggled", self.reload_fil_treestore, "freq")
        button.set_active(True)
        vbox.pack_start(button, False, False, 0)
        button.show()

        button = gtk.RadioButton(button, "dataflow volume")
        button.connect("toggled", self.reload_fil_treestore, "datafl")
        vbox.pack_start(button, False, False, 0)
        button.show()
        
        # Menu for data type
        label = gtk.Label('Include counters:')
        vbox.pack_start(label, False, False, 5)
        label.show()

        button = gtk.RadioButton(None, "read")
        button.connect("toggled", self.reload_fil_treestore, "r")
        button.set_active(True)
        vbox.pack_start(button, False, False, 0)
        button.show()

        button = gtk.RadioButton(button, "write")
        button.connect("toggled", self.reload_fil_treestore, "w")
        vbox.pack_start(button, False, False, 0)
        button.show()

        button = gtk.RadioButton(button, "read + write")
        button.connect("toggled", self.reload_fil_treestore, "r+w")
        vbox.pack_start(button, False, False, 0)
        button.show()

        vbox.show()
        table.attach(frame, 5, 6, 0, 3)
        frame.show()
        table.show()

        label = gtk.Label('Files')
        notebook.append_page(table, label)

        # =============== Pages added ===============

        # Set what page to start at (page 1)
        notebook.set_current_page(0)

        notebook.show()
        window.show()

    def reload_proc_treestore(self, widget, data=None):
        if not data[0] == None:
            self.proc_show = data[0]
        if not data[1] == None:
            self.proc_counter = data[1]

        self.proc_treestore.clear()
        
        if self.proc_show == 'freq':
            for pd in self.all_data.get_proc_data_list():
                pointer = self.proc_treestore.append(None, [pd.get_name(), 'x files', str(pd.get_frequency(self.proc_counter)) + ' Hz'])
        else:
            for pd in self.all_data.get_proc_data_list():
                pointer = self.proc_treestore.append(None, [pd.get_name(), 'x files', str(pd.get_dataflow(self.proc_counter)) + ' B'])

    def reload_part_treestore(self, widget, data=None):
        if not data[0] == None:
            self.part_show = data[0]
        if not data[1] == None:
            self.part_counter = data[1]

        self.part_treestore.clear()

        if self.part_show == 'freq':
            for pd in self.all_data.get_part_data_list():
                pointer = self.part_treestore.append(None, [pd.get_name(), 'x files', str(pd.get_frequency(self.part_counter)) + ' Hz'])
        else:
            if self.part_show == 'datafl':
                for pd in self.all_data.get_part_data_list():
                    pointer = self.part_treestore.append(None, [pd.get_name(), 'x files', str(pd.get_dataflow(self.part_counter)) + ' B'])
            else:
                for pd in self.all_data.get_part_data_list():
                    pointer = self.part_treestore.append(None, [pd.get_name(), 'x files', str(pd.get_time(self.part_counter)) + ' ms'])

    def reload_fil_treestore(self, widget, data=None):
        #for pd in self.all_data.get_proc_data_list():
            #pointer = self.part_treestore.append(None, [pd.get_name(), 'x files', str(pd.get_frequency()) + ' Hz'])
        pass

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    MainWindow()
    main()

