from enum import Enum

nice_table = {
    -20: 88761, -19: 71755, -18: 56483, -17: 46273, -16: 36291,
    -15: 29154, -14: 23254, -13: 18705, -12: 14949, -11: 11916,
    -10: 9548, -9: 7620, -8: 6100, -7: 4904, -6: 3906,
    -5: 3121, -4: 2501, -3: 1991, -2: 1586, -1: 1277,
    0: 1024, 1: 820, 2: 655, 3: 526, 4: 423,
    5: 335, 6: 272, 7: 215, 8: 172, 9: 137,
    10: 110, 11: 87, 12: 70, 13: 56, 14: 45,
    15: 36, 16: 29, 17: 23, 18: 18, 19: 15}

Policy = Enum('Policy', ["SCHED_FIFO", "SCHED_RR", "SCHED_NORMAL"])

class Task:
    def __init__(self, pid, sched_policy, arrival_time, burst_time) -> None:
        # info the scheduler shouldn't know
        self.burst_time = burst_time

        # infor the scheduler should know
        self.pid = pid
        self.sched_policy = Enum('Policy', ['SCHED_RR', 'SCHED_FIFO', 'SCHED_NORMAL'])
        self.sched_policy = sched_policy
        self.arrival_time = arrival_time

        self.exec_time = 0
        self.response_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.first_time_scheduled = True


class Realtime (Task): 
    def __init__(self, pid, sched_policy, priority, arrivial_time, burst_time) -> None:
        super().__init__(pid, sched_policy, arrivial_time, burst_time)
        self.priority = priority
        self.sched_policy = sched_policy

    # real-time task doesn't have virtual runtime
    def update_if_executed(self, exec_time):
        self.exec_time += exec_time
        self.burst_time -= exec_time
        self.turnaround_time += exec_time

    def update_if_in_queue(self, exec_time):
        self.waiting_time += exec_time
        self.turnaround_time += exec_time

class Normal (Task):
    def __init__(self, pid, nice, arrival_time, burst_time) -> None:
        super().__init__(pid, Policy.SCHED_NORMAL, arrival_time, burst_time)
        self.nice = nice
        # print(f"nice = {nice}")
        self.weight = nice_table [self.nice]
        self.vruntime = 0
    
    def update_period (self, nr_running, sched_latency, min_granularity):     # the calculation's already considered priority
        self.period = sched_latency / nr_running
        if (self.period < min_granularity) : self.period = min_granularity
        # self.period = self.period * self.weight / load_weight     # period for each thread also depends on priority
    
    def update_vruntime (self, vruntime_rate):
        # tasks with higher weight (priority) accumulate vruntime with slower rate -> get to run more
        self.vruntime = self.exec_time * 1024.0 / self.weight * vruntime_rate

    def update_if_executed(self, exec_time, vruntime_rate):
        self.exec_time += exec_time
        self.burst_time -= exec_time
        self.turnaround_time += exec_time
        self.update_vruntime(vruntime_rate)

    def update_if_in_queue(self, exec_time):
        self.waiting_time += exec_time
        self.turnaround_time += exec_time