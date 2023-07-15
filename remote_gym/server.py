import json_numpy
json_numpy.patch()
from .serialization import serialize_space

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from dataclasses import dataclass
from typing import Any, Dict

import numpy as np
import uvicorn

import logging
import gym
import uuid

def json_response(obj):
    return JSONResponse(json_numpy.dumps(obj))

class Server:
    """ A simple server for many Gym environments.
    
    Use /make to create a new environment with a given name and kwargs.
        - Takes in {'env_name': str, 'env_kwargs': Dict[str, Any]}
        - Returns {'instance_id': int, 'observation_space': Space, 'action_space': Space}

    Use /reset to reset an environment.
        - Takes in {'instance_id': int}
        - Returns {'observation': np.ndarray}

    Use /step to step an environment with a given action.
        - Takes in {'instance_id': int, 'action': Any}
        - Returns {'next_observation': np.ndarray, 'reward': float, 'done': bool, 'info': Dict[str, Any]}
    """
    def __init__(self):
        self.envs = {}

    def run(self, port=8000, host='0.0.0.0'):
        self.app = FastAPI()
        self.app.post("/make")(self.create_env)
        self.app.post("/step")(self.step)
        self.app.post("/reset")(self.reset)
        self.app.get("/info")(self.get_info)

        uvicorn.run(self.app, host=host, port=port)  


    def create_env(self, payload: Dict[Any, Any]):
        env_name = payload['env_name']
        kwargs = payload['env_kwargs']
        env = gym.make(env_name, **kwargs)
        id = uuid.uuid1().int
        self.envs[id] = env
        return json_response({
            'instance_id': id,
            'observation_space': serialize_space(env.observation_space),
            'action_space': serialize_space(env.action_space),
        })

    def get_info(self, instance_id: int):
        env = self.envs[instance_id]
        return json_response({
            'observation_space': serialize_space(env.observation_space),
            'action_space': serialize_space(env.action_space),
        })

    def step(self, payload: Dict[Any, Any]):
        instance_id = payload['instance_id']
        action = payload['action']

        logging.warning(f'Stepping in instance {instance_id}')
        logging.warning(f'Action: {action}')

        ns, r, done, info = self.envs[instance_id].step(action)
        return_dict = {
            'next_observation': ns,
            'reward': r,
            'done': done,
            'info': info,
        }
        return json_response(return_dict)
    
    def reset(self, payload: Dict[Any, Any]):
        instance_id = payload['instance_id']
        logging.warning(f'Resetting in instance {instance_id}')
        o = self.envs[instance_id].reset()
        return_dict = {'observation': o}
        return json_response(return_dict)

def main():
    server = Server()
    server.run()

if __name__ == "__main__":
    main()