from setuptools import find_packages, setup

setup(
    name='thingooConnector',
    packages=find_packages(include=['thingooConnector']),
    version='0.0.1',
    description='ThingooConnector',
    author='KNI',
    install_requires=['requests', 'paho-mqtt'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
