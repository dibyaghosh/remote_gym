import json_numpy
json_numpy.patch()
import json

import gym

loads = json.loads

def deserialize_space(space_def):
    if space_def['type'] == 'Discrete':
        return gym.spaces.Discrete(space_def['n'])
    elif space_def['type'] == 'Box':
        return gym.spaces.Box(
            low=space_def['low'],
            high=space_def['high'],
            dtype=space_def['dtype']
        )
    elif space_def['type'] == 'Dict':
        return gym.spaces.Dict({k: deserialize_space(v) for k, v in space_def['spaces'].items()})
    else:
        raise ValueError(f'Unknown space type: {space_def["type"]}')

def serialize_space(space):
    if isinstance(space, gym.spaces.Discrete):
        return {
            'type': 'Discrete',
            'n': space.n
        }
    elif isinstance(space, gym.spaces.Box):
        return {
            'type': 'Box',
            'low': space.low,
            'high': space.high,
            'dtype': str(space.dtype)
        }
    elif isinstance(space, gym.spaces.Dict):
        return {
            'type': 'Dict',
            'spaces': {k: serialize_space(v) for k, v in space.spaces.items()}
        }
    else:
        raise ValueError(f'Unknown space type: {type(space)}')