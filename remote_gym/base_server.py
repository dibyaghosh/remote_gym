import logging
import gym
import uuid
import time

class Server:
    """ Managing many gym environments (with LRU cache)
    """
    def __init__(self, max_parallel_envs=20):
        self.envs = {}
        self.last_used = {}
        self.max_parallel_envs = max_parallel_envs

    def get_env(self, env_id):
        assert env_id in self.envs
        self.last_used[env_id] = time.time()
        return self.envs[env_id]

    def clean_envs(self):
        while len(self.envs) > self.max_parallel_envs:
            oldest_env_id = min(self.last_used, key=self.last_used.get)
            logging.warning(f'Deleting environment {self.envs[oldest_env_id]} since max_parallel_envs exceeded')
            del self.envs[oldest_env_id]
            del self.last_used[oldest_env_id]

    def create_env(self, env_name, env_kwargs):
        self.clean_envs()
        env = gym.make(env_name, **env_kwargs)
        logging.warning(f'Created environment {env_name}({env_kwargs})')
        id = str(uuid.uuid1())
        self.envs[id] = env
        self.last_used[id] = time.time()
        return (id, env)

    def step(self, env_id, action):
        return self.get_env(env_id).step(action)
    
    def reset(self, env_id):
        return self.get_env(env_id).reset()
