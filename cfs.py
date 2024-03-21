'''
Works to do:
    - Implement a clock to give back control to OS when timeslice exceeded?
'''

import numpy as np
from sortedcontainers import SortedKeyList
from task import Task, Normal, Realtime

MIGRATION_COST = 0.5
NR_MIGRATE = 32


class CFSScheduler:
    def __init__(self, task_list) -> None:
        self.task_list = task_list[1:]
        self.tasks_sorted = SortedKeyList (key = lambda task: task.vruntime)
        fst_task = task_list[0]
        self.tasks_sorted.add(fst_task)
        self.start_time = fst_task.arrival_time
        self.timer = self.start_time
        self.min_vruntime = 0
        self.load_weight = fst_task.weight
        self.nr_running = 1

    def update_load_weight (self, task_weight):
        self.load_weight += task_weight

    def execute_norm_task (self, task : Normal):
        task.update_period(self.nr_running, self.load_weight)
        if (task.burst_time < task.period): exec_time = task.burst_time
        else: exec_time = task.period
        self.timer += exec_time

        # accumulate exec time and properties of current task
        task.update_if_executed(exec_time)

        # update properties for tasks remained in queue
        for queue_task in self.tasks_sorted[1:]:
            queue_task.update_if_in_queue(exec_time)
        
        # remove task from list if done, otherwise reorder the list base on vruntime
        self.tasks_sorted.pop(0)
        if (task.burst_time > 0): self.tasks_sorted.add(task)
        else: 
            self.nr_running -= 1
            self.load_weight -= task.weight
            self.print_proc_in_queue()

    def print_proc_in_queue (self):
        print (f"TIMER: {self.timer} -- CURRENT PROCESSES IN READY QUEUE (VRUNTIME ASCENDED)")
        print ("pid, vruntime, executed time, reponse time, waiting time, remaining time")
        print ("==========================================================")
        for task in self.tasks_sorted:
            print (f"{task.pid}, {task.vruntime}, {task.exec_time}, {task.response_time}, {task.waiting_time}, {task.burst_time}")
        print("\n")
        
    def cfs_schedule (self):   # task_list is sorted based on arrival time
        while (len(self.task_list) > 0 or len(self.tasks_sorted) > 0):
            if (len(self.task_list) > 0):
                next_arrived_task = self.task_list[0]
                if (next_arrived_task.arrival_time <= self.timer):
                    self.task_list.pop(0)
                    self.tasks_sorted.add(next_arrived_task)
                    next_arrived_task.waiting_time = self.timer
                    next_arrived_task.turnaround_time = self.timer
                    next_arrived_task.response_time = self.timer
                    next_arrived_task.vruntime = self.min_vruntime
                    self.nr_running += 1
                    self.load_weight += next_arrived_task.weight
                    self.update_load_weight(next_arrived_task.weight)
                    self.print_proc_in_queue()

            next_exec_task = self.tasks_sorted[0]
            self.execute_norm_task (next_exec_task)
            if (len(self.tasks_sorted) == 0):
                if (len(self.task_list) > 0):
                    self.timer = self.task_list[0].arrival_time      # speed up timer when there's no task in ready queue
                    self.min_vruntime = 0
            else:
                self.min_vruntime = self.tasks_sorted[0].vruntime
            