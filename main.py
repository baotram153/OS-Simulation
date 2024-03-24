'''
Works to do:
    - Input: Processes in ready queue -> [nice, exec_time, waiting_time, response time, vruntime]
    - Reward: Average waiting time, turnaround time, response time improved by 10% -> +1
    - Output: latency, min_granularity, vruntime_rate
    - Implement a clock to give back control to OS when timeslice exceeded?
'''

import data_generator, cfs
import ray
from ray.tune.logger import pretty_print
from ray.rllib.algorithms import ppo
from env import OSEnv

SEC_TO_MS = 1000000

class Test:
    def __init__(self, NR_TASK, NICE_MU, NICE_SIGMA, ARRIVAL_MU, ARRIVAL_SIGMA, BURST_MU, BURST_SIGMA) -> None:
        self.env_config = {}
        self.env_config["NR_TASK"] = NR_TASK
        self.env_config["NICE_MU"] = NICE_MU
        self.env_config["NICE_SIGMA"] = NICE_SIGMA
        # self.ARRIVAL_MU = 1*SEC_TO_MS    # second
        # self.ARRIVAL_SIGMA = 0.5*SEC_TO_MS
        # self.BURST_MU = 4*SEC_TO_MS
        # self.BURST_SIGMA = 2*SEC_TO_MS
        self.env_config["ARRIVAL_MU"] = ARRIVAL_MU    # second
        self.env_config["ARRIVAL_SIGMA"] = ARRIVAL_SIGMA
        self.env_config["BURST_MU"] = BURST_MU
        self.env_config["BURST_SIGMA"] = BURST_SIGMA
        self.env = OSEnv(data_config = self.env_config)

    def test_cfs_scheduling(self):
        ray.init()
        algo = ppo.PPO(env=OSEnv, config={
            "env_config": self.env_config,  # config to pass to env class
        })
        for i in range(10):
            result = algo.train()
            print(pretty_print(result))

            if i % 5 == 0:
                checkpoint_dir = algo.save().checkpoint.path
                print(f"Checkpoint saved in directory {checkpoint_dir}")
        

# params
NR_TASK = 10
NICE_MU = 0
NICE_SIGMA = 5
# self.ARRIVAL_MU = 1*SEC_TO_MS    # second
# self.ARRIVAL_SIGMA = 0.5*SEC_TO_MS
# self.BURST_MU = 4*SEC_TO_MS
# self.BURST_SIGMA = 2*SEC_TO_MS
ARRIVAL_MU = 5    # microsecond
ARRIVAL_SIGMA = 2
BURST_MU = 50
BURST_SIGMA = 20

test = Test(NR_TASK, NICE_MU, NICE_SIGMA, ARRIVAL_MU, ARRIVAL_SIGMA, BURST_MU, BURST_SIGMA)
test.test_cfs_scheduling()