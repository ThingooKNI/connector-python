from setuptools import find_packages, setup

setup(
    name='thingoo-connector-python',
    packages=find_packages(include=['requests']),
    version='0.0.1',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
