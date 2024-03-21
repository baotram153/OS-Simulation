# from task import Task, Normal, Realtime
import task
import numpy as np

SEC_TO_MS = 1000000

class TaskListGenerator:
    def __init__(self) -> None:
        self.task_list = []
        self.NR_TASK = 10
        self.NICE_MU = 0
        self.NICE_SIGMA = 5
        # self.ARRIVAL_MU = 1*SEC_TO_MS    # second
        # self.ARRIVAL_SIGMA = 0.5*SEC_TO_MS
        # self.BURST_MU = 4*SEC_TO_MS
        # self.BURST_SIGMA = 2*SEC_TO_MS
        self.ARRIVAL_MU = 5    # second
        self.ARRIVAL_SIGMA = 2
        self.BURST_MU = 50
        self.BURST_SIGMA = 20

    def generate_normal_tasks (self):
        for i in range (self.NR_TASK):
            nice = np.rint(max(min(np.random.normal(self.NICE_MU, self.NICE_SIGMA), 20), -19))
            arrival_time = max (np.random.normal(self.ARRIVAL_MU, self.ARRIVAL_SIGMA), 0)
            burst_time = max (np.random.normal(self.BURST_MU, self.BURST_SIGMA), 0)
            new_task = task.Normal (i, nice, arrival_time, burst_time)
            self.task_list.append(new_task)
        self.write_task_lists()

    def generate_realtime_tasks (self):
        pass

    def generate_mix_tasks (self):
        pass

    def print_task_lists(self):
        print("TASK LIST")
        print("======================================================")
        for task in self.task_list:
            print(f"{task.pid}, {task.nice}, {task.arrival_time}, {task.burst_time}")

    def write_task_lists(self):
        f = open("data.txt", "w")
        f.write("TASK LIST \n")
        f.write("pid, nice, arrival_time, burst_time")
        f.write("====================================================== \n")
        for task in self.task_list:
            f.write(f"{task.pid}, {task.nice}, {task.arrival_time}, {task.burst_time} \n")
        f.close()

if __name__ == "__main__":
    task_list = TaskListGenerator()
    task_list.generate_normal_tasks()
    task_list.print_task_lists()