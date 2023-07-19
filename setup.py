from setuptools import setup, find_packages
setup(
    name="remote_gym",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'remote_gym_server = remote_gym.http_server:main',
        ]
    },
    install_requires=[
        "uvicorn",
        "fastapi",
        "requests",
        "json-numpy",
    ],     
)