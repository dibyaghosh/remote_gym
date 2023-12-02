import json_numpy
json_numpy.patch()
from .serialization import serialize_space
from .base_server import Server
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from dataclasses import dataclass
from typing import Any, Dict

import uvicorn
import logging


def json_response(obj):
    return JSONResponse(json_numpy.dumps(obj))

class HttpServer:
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
    def __init__(self, base_server: Server = None):
        self.base_server = base_server or Server()

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
        id, env = self.base_server.create_env(env_name, kwargs)
        return json_response({
            'instance_id': id,
            'observation_space': serialize_space(env.observation_space),
            'action_space': serialize_space(env.action_space),
        })

    def get_info(self, instance_id: str):
        env = self.base_server.get_env(instance_id)
        return json_response({
            'observation_space': serialize_space(env.observation_space),
            'action_space': serialize_space(env.action_space),
        })

    def step(self, payload: Dict[Any, Any]):
        instance_id = payload['instance_id']
        action = payload['action']
        ns, r, done, info = self.base_server.step(instance_id, action)
        return json_response({
            'next_observation': ns,
            'reward': r,
            'done': done,
            'info': info,
        })
    
    def reset(self, payload: Dict[Any, Any]):
        instance_id = payload['instance_id']
        o = self.base_server.reset(instance_id)
        return json_response({'observation': o})

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Host to run on", default="0.0.0.0", type=str)
    parser.add_argument("--port", help="Port to run on", default=8000, type=int)
    args = parser.parse_args()
    server = HttpServer()
    server.run(args.port, args.host)

if __name__ == "__main__":
    main()