import psutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class ProcessMonitorGUI:
    """Class to create and manage the process monitor GUI."""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Process Monitor")
        self.root.geometry("1000x600")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.processes = {}
        self.selected_process = None
        self.sort_by = tk.StringVar(value="cpu_percent")
        self.filter_by = tk.StringVar(value="all")

        self.create_widgets()
        self.update_process_list()
        self.root.mainloop()

    def create_widgets(self):
        """Create the GUI widgets."""
        main_frame = ttk.Frame(self.root)
        main_frame.grid(column=0, row=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(main_frame, columns=('Name', 'PID', 'Status', 'CPU %', 'Memory Usage', 'Command Line'), show='headings')
        self.tree.column('Name', width=200, anchor='w')
        self.tree.column('PID', width=80, anchor='center')
        self.tree.column('Status', width=80, anchor='center')
        self.tree.column('CPU %', width=80, anchor='center')
        self.tree.column('Memory Usage', width=120, anchor='center')
        self.tree.column('Command Line', width=400, anchor='w')
        self.tree.heading('Name', text='Name')
        self.tree.heading('PID', text='PID')
        self.tree.heading('Status', text='Status')
        self.tree.heading('CPU %', text='CPU %')
        self.tree.heading('Memory Usage', text='Memory Usage')
        self.tree.heading('Command Line', text='Command Line')
        self.tree.bind("<ButtonRelease-1>", self.select_process)
        self.tree.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.label = ttk.Label(self.root, text="")
        self.label.grid(row=1, column=0, sticky='w')

        self.terminate_button = ttk.Button(self.root, text="Terminate Process", state=tk.DISABLED, command=self.terminate_process)
        self.terminate_button.grid(row=1, column=0, sticky='e')

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.sort_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.sort_menu.add_radiobutton(label="CPU %", variable=self.sort_by, value="cpu_percent", command=self.update_process_list)
        self.sort_menu.add_radiobutton(label="Memory Usage", variable=self.sort_by, value="memory_info", command=self.update_process_list)
        self.sort_menu.add_radiobutton(label="Process Name", variable=self.sort_by, value="name", command=self.update_process_list)
        self.menu_bar.add_cascade(label="Sort By", menu=self.sort_menu)

        self.filter_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.filter_menu.add_radiobutton(label="All Processes", variable=self.filter_by, value="all", command=self.update_process_list)
        self.filter_menu.add_radiobutton(label="Running Processes", variable=self.filter_by, value="running", command=self.update_process_list)
        self.filter_menu.add_radiobutton(label="Non-Running Processes", variable=self.filter_by, value="nonrunning", command=self.update_process_list)
        self.menu_bar.add_cascade(label="Filter By", menu=self.filter_menu)

    def update_process_list(self):
        """Update the list of running processes."""
        self.tree.delete(*self.tree.get_children())
        self.processes.clear()

        proc_attrs = ['pid', 'name', 'status', 'cpu_percent', 'memory_info', 'cmdline']
        all_processes = psutil.process_iter(attrs=proc_attrs)

        if self.filter_by.get() == "running":
            processes = [p for p in all_processes if p.info['status'] == psutil.STATUS_RUNNING]
        elif self.filter_by.get() == "nonrunning":
            processes = [p for p in all_processes if p.info['status'] != psutil.STATUS_RUNNING]
        else:
            processes = list(all_processes)

        processes = sorted(processes, key=lambda p: p.info[self.sort_by.get()], reverse=True)

        for process in processes:
            process_info = self.get_process_info(process)
            if process_info:
                self.processes[process_info['pid']] = process_info
                self.tree.insert('', 'end', text=process_info['pid'], values=(process_info['name'], process_info['pid'], process_info['status'], process_info['cpu_percent'], process_info['memory_usage'], process_info['command_line']))

        self.update_label(len(processes))
        self.root.after(1000, self.update_process_list)

    def get_process_info(self, process):
        try:
            pid = process.info['pid']
            name = process.info['name']
            status = process.info['status']
            cpu_percent = process.info['cpu_percent']
            memory_info = process.info['memory_info']

            memory_usage = psutil._common.bytes2human(memory_info.rss)

            if process.info['cmdline'] is not None and len(process.info['cmdline']) > 0:
                command_line = ' '.join(process.info['cmdline'])
            else:
                command_line = ""

            return {'pid': pid, 'name': name, 'status': status, 'cpu_percent': cpu_percent, 'memory_usage': memory_usage, 'command_line': command_line}
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print(f"Error getting process info: {e}")
            return {}

    def update_label(self, num_processes):
        self.label.config(text=f"Number of running processes: {num_processes}")

    def select_process(self, event):
        pid = self.tree.item(self.tree.selection())['text']
        if pid in self.processes:
            self.selected_process = pid
            self.terminate_button.config(state=tk.NORMAL)
        else:
            self.selected_process = None
            self.terminate_button.config(state=tk.DISABLED)

    def terminate_process(self):
        if self.selected_process in self.processes:
            process_info = self.processes[self.selected_process]
            if messagebox.askyesno("Terminate Process", f"Are you sure you want to terminate {process_info['name']} (PID {process_info['pid']})?"):
                try:
                    process = psutil.Process(self.selected_process)
                    process.terminate()
                    self.selected_process = None
                    self.terminate_button.config(state=tk.DISABLED)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                    messagebox.showerror("Error", f"Error terminating process: {e}")
        else:
            self.selected_process = None
            self.terminate_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    gui = ProcessMonitorGUI()
