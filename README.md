# Remote Gym

Utility to run gym environments from a different location than the agent. Useful if environment has been installed:

- in a different conda environment
- in a Docker container
- even a different machine (over ssh)!

## Quick Setup

On both the remote and local client, install the package:

```bash
pip install git+https://github.com/dibyaghosh/remote_gym.git
```

On the remote client, start the server:

```bash
remote_gym_server # starts the server on port 8000
```

On the local client, you can now connect:
```python
from remote_gym.client import RemoteEnv
env = RemoteEnv.make('CartPole-v0', url='0.0.0.0:8000')
```

## Docker Setup

A Dockerfile is provided to run the server in a Docker container. 

```bash
docker run -p 8000:8000 --gpus all -it dibyaghosh/docker_gym_base
```

If you want to put your own environment in the container, you can simply start from this base image and install your own environment:

```dockerfile
FROM dibyaghosh/docker_gym_base
pip install your_env
```
