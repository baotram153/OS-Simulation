from scheduler.scheduler import Scheduler

'''
Real-time Scheduling
    - Priority from 0-99
    - Two types of policies: SCHED_FIFO and SCHED_RR (RR just like FIFO but using RR for tasks with the same priority)
    - 
'''

class RealtimeScheduler (Scheduler):
    def __init__(self, task_list) -> None:
        super().__init__()
        
