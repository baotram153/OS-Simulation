import numpy as np


class Scheduler:
    def __init__(self) -> None:
        self.all_tasks_done = []
        self.FEEDBACK_PERIOD = 200    # microsecond
        self.nth_feedback = 1
        self.tasks_to_feedback = []

    def calc_avg(self, task_list):
        avg_response_time = np.average([task.response_time for task in task_list])
        avg_waiting_time = np.average([task.waiting_time for task in task_list])
        avg_turnaround_time = np.average([task.turnaround_time for task in task_list])
        task_list.clear()
        return np.array([avg_response_time, avg_waiting_time, avg_turnaround_time])
    
    def print_avg(self, task_list):
        nr_tasks = len(task_list)
        avg_response_time, avg_waiting_time, avg_turnaround_time = self.calc_avg(task_list)
        print("CALCULATE AVERAGE")
        print("==========================================")
        print(f"- Number of tasks: {nr_tasks}")
        print(f"- Average response time: {avg_response_time}")
        print(f"- Average waiting time: {avg_waiting_time}")
        print(f"- Average turnaround time: {avg_turnaround_time}")
        print("\n")