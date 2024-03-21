import data_generator, cfs
from sortedcontainers import SortedKeyList

class Test:
    def __init__(self) -> None:
        self.generator = data_generator.TaskListGenerator()   # should be modified to enable argument passing

    def test_cfs_scheduling(self):
        self.generator.generate_normal_tasks()
        task_list_sorted = SortedKeyList(self.generator.task_list, key= lambda x : x.arrival_time)
        scheduler = cfs.CFSScheduler(task_list_sorted)
        scheduler.cfs_schedule()

test = Test()
test.test_cfs_scheduling()