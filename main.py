'''
Works to do:
    - Input: Processes in ready queue -> [nice, exec_time, waiting_time, response time, vruntime]
    - Reward: Average waiting time, turnaround time, response time improved by 10% -> +1
    - Output: latency, min_granularity, vruntime_rate
    - Implement a clock to give back control to OS when timeslice exceeded?
'''

import data_generator, scheduler.cfs as cfs
from ray import tune
from ray.tune.logger import pretty_print
from ray.rllib.algorithms import PPOConfig
from env import OSEnv
import time

SEC_TO_MS = 1000000

class Test:
    def __init__(self, N_ITERATIONS, NR_TASK, NICE_MU, NICE_SIGMA, ARRIVAL_MU, ARRIVAL_SIGMA, BURST_MU, BURST_SIGMA) -> None:
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
        # self.env = OSEnv(env_config = self.env_config)
        self.env_config["N_ITERATIONS"] = N_ITERATIONS
        self.N_ITERATIONS = N_ITERATIONS

    def test_cfs_scheduling(self, plot = False):
        algo = (
            PPOConfig()
            .rollouts(num_rollout_workers=1, batch_mode= "truncate_episodes")
            .resources(num_gpus=0)
            .environment(env=OSEnv, env_config= self.env_config)
            .build()
        )
        for i in range(self.N_ITERATIONS):
            print(f"Iteration {i}=======================================")
            time.sleep(2)
            result = algo.train()
            print(pretty_print(result))

            checkpoint_dir = algo.save().checkpoint.path
            print(f"Checkpoint saved in directory {checkpoint_dir}")

        # tune.run(
        # "PPO",
        # checkpoint_freq=10,
        # config={
        #     "env": OSEnv,
        #     "entropy_coeff": 0.01,
        #     "train_batch_size": 5000,
        #     "sample_batch_size": 100,
        #     "sgd_minibatch_size": 500,
        #     "num_workers": 1,
        #     "num_envs_per_worker": 1,
        #     "gamma": 0.95,
        #     "batch_mode": "complete_episodes",
        #     "num_gpus": 1,
        #     "env_config": self.env_config
        #     })

    def test_baseline(self, n_iterations, plot = False):
        env = OSEnv(self.env_config)
        env.test_baseline(n_iterations, plot)
        

# params
N_ITERATIONS = 10
NR_TASK = 10
NICE_MU = 0
NICE_SIGMA = 10
# self.ARRIVAL_MU = 1*SEC_TO_MS    # second
# self.ARRIVAL_SIGMA = 0.5*SEC_TO_MS
# self.BURST_MU = 4*SEC_TO_MS
# self.BURST_SIGMA = 2*SEC_TO_MS
ARRIVAL_MU = 50    # microsecond
ARRIVAL_SIGMA = 20
BURST_MU = 60
BURST_SIGMA = 20

test = Test(N_ITERATIONS, NR_TASK, NICE_MU, NICE_SIGMA, ARRIVAL_MU, ARRIVAL_SIGMA, BURST_MU, BURST_SIGMA)
# test.test_cfs_scheduling()
test.test_baseline(1, True)