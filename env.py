import gymnasium as gym
import numpy as np
import cfs
import data_generator
from sortedcontainers import SortedKeyList
from copy import deepcopy

class OSEnv (gym.Env) :
    def __init__(self, data_config) -> None:     # data_config is a dictionary
        # data_config (work load) is fixed when training
        super().__init__()
        self.STATE_SPACE_DIM = 10
        self.ACTION_MEAN = [24, 3, 1]      # latency, min_granularity, vruntime_rate
        self.ACTION_STD = [1, 1, 1]
        self.action_space = gym.spaces.Box(low = -1, high=1, dtype=np.float32, shape=(3,))
        self.OBSERVATION_MIN = np.zeros((self.STATE_SPACE_DIM, 5))    # nice, exec time, response time, waiting time, vruntime
        self.OBSERVATION_MIN[:,0] = -20
        self.OBSERVATION_MAX = np.multiply(np.ones((self.STATE_SPACE_DIM, 5)),np.array([19, 2000, 1000, 1000, 2000]))
        self.observation_space = gym.spaces.Box(low = -1, high = 1, shape= (self.STATE_SPACE_DIM, 5))
        self.RES_MAX = [1000, 2000, 2000]    # avg response time, avg waiting time, avg turnaround time

        self.generator = data_generator.TaskListGenerator(data_config)   # should be modified to enable argument passing         

    def calc_reward (self, new_res) -> float:
        if (len(new_res) == 0 or len(self.old_res) == 0): return 0    # happen when there're no tasks done in a time period
        improve_rate = np.sum(new_res) / np.sum(self.old_res)
        if (improve_rate < 0.9): reward = 1
        elif (improve_rate > 1.1): reward = -1
        else: reward = 0
        self.old_res = new_res
        return reward

    def data_generate(self):
        self.generator.generate_normal_tasks()  # task configures have been applied to generator
        task_list_sorted = SortedKeyList(self.generator.task_list, key= lambda x : x.arrival_time)
        return task_list_sorted

    def list_to_mat(self, observation_list):  # (self.DIM, 5)
        observation_mat = [[x.nice, x.exec_time, x.response_time, x.waiting_time, x.vruntime] for x in observation_list]
        return np.array(observation_mat)
    
    def padding (self, mat):    # state matrix have fixed length of 10 -> pad with zeros if there're < 10 processes
        padded_mat = mat
        padding_row = np.zeros((1, 5))  # change the padding_row later
        if (mat.shape[0] == 0):
            padded_mat = np.zeros((self.STATE_SPACE_DIM, 5))
        elif (mat.shape[0] < self.STATE_SPACE_DIM):
            nr_padding_rows = self.STATE_SPACE_DIM - mat.shape[0]
            padding_mat = np.multiply(np.ones((nr_padding_rows, 5)), padding_row)
            padded_mat = np.concatenate((mat, padding_mat), axis = 0)
        return padded_mat

    def reset (self, seed = None, options = None ):
        self.old_res = self.RES_MAX
        task_list_sorted = self.data_generate()
        self.scheduler = cfs.CFSScheduler(task_list_sorted)
        # scheduler.cfs_schedule()
        print(task_list_sorted)
        return self.rescale_ob(self.OBSERVATION_MAX), {}

    def step (self, action):
        rescale_action = self.rescale_action(action)
        observation_list, new_res, terminated = self.scheduler.cfs_schedule_until_feedback(rescale_action)
        observation_mat_padded = self.padding(self.list_to_mat(observation_list))
        new_observation = self.rescale_ob(observation_mat_padded)
        reward = self.calc_reward (new_res)
        return new_observation, reward, terminated, False, {}
    
    def rescale_ob(self, observation):  # rescale from (min, max) to (-1, 1)
        return (deepcopy(observation) - self.OBSERVATION_MIN) / (self.OBSERVATION_MAX - self.OBSERVATION_MIN)*2 - 1

    def rescale_action(self, action):
        return deepcopy(action)*self.ACTION_STD + self.ACTION_MEAN