import requests
import urllib.parse
import numpy as np
import gym
import logging
from .serialization import deserialize_space, loads

class RemoteEnv(gym.Env):
    """ A simple client for the Gym server. """
    
    @classmethod
    def make(cls, env_name, url='http://localhost:8000', **kwargs):
        logging.warning(f'Creating remote environment {env_name} with kwargs {kwargs}')
        response = loads(requests.post(
            urllib.parse.urljoin(url, 'make'),
            json={'env_name': env_name, 'env_kwargs': kwargs}
        ).json())
        logging.warning(f'Created env with instance_id {response["instance_id"]}')
        return cls(response['instance_id'], url=url)

    def __init__(self, instance_id, url='http://localhost:8000'):
        self.url = url
        self.instance_id = instance_id

        response = self.info()
        self.observation_space = deserialize_space(response['observation_space'])
        self.action_space = deserialize_space(response['action_space'])
        logging.warning(f'Connected to remote environment with observation space {self.observation_space} and action space {self.action_space}')

    def query_endpoint(self, endpoint, data, method='POST'):
        if method == 'POST':
            response = requests.post(
                urllib.parse.urljoin(self.url, endpoint),
                json={**data, 'instance_id': self.instance_id}
            )
        elif method == 'GET':
            response = requests.get(
                urllib.parse.urljoin(self.url, endpoint),
                params={**data, 'instance_id': self.instance_id}
            )
        
        return loads(response.json())
    
    def info(self):
        return self.query_endpoint('info', {}, method='GET')
    
    def reset(self):
        response = self.query_endpoint('reset', {})
        return response['observation']

    def step(self, action):
        response = self.query_endpoint('step', {'action': action})
        return response['next_observation'], response['reward'], response['done'], response['info']