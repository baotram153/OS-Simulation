# from task import Task, Normal, Realtime
import task
import numpy as np

SEC_TO_MS = 1000000

class TaskListGenerator:
    def __init__(self, env_config) -> None:
        self.task_list = []
        self.NR_TASK = env_config["NR_TASK"]
        self.NICE_MU = env_config["NICE_MU"]
        self.NICE_SIGMA = env_config["NICE_SIGMA"]
        self.ARRIVAL_MU = env_config["ARRIVAL_MU"]    # microsecond
        self.ARRIVAL_SIGMA = env_config["ARRIVAL_SIGMA"]
        self.BURST_MU = env_config["BURST_MU"]
        self.BURST_SIGMA = env_config["BURST_SIGMA"]

    def generate_normal_tasks (self):
        self.task_list = []
        for i in range (self.NR_TASK):
            nice = np.rint(max(min(np.random.normal(self.NICE_MU, self.NICE_SIGMA), 19), -20))
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
        f.write("pid, nice, arrival_time, burst_time \n")
        f.write("====================================================== \n")
        for task in self.task_list:
            f.write(f"{task.pid}, {task.nice}, {task.arrival_time}, {task.burst_time} \n")
        f.close()

# if __name__ == "__main__":
#     task_list = TaskListGenerator()
#     task_list.generate_normal_tasks()
#     task_list.print_task_lists()