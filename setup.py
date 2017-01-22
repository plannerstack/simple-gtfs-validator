from setuptools import setup
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='simple-gtfs-validator',
    version='0.1',
    install_requires=requirements,
    scripts=['gtfs_fare_validator']
)