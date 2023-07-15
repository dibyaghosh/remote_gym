from setuptools import setup, find_packages

setup(
    name="docker_gym",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'docker_gym_server = docker_gym.server:main',
        ]
    }
)