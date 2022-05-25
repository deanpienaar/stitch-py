from setuptools import find_packages, setup


with open('./requirements/base.txt') as f:
    requirements = f.read().split('\n')


setup(
    name='stitch_sdk',
    version='v0.0.2',
    description='Unofficial Stitch Python SDK',
    install_requires=requirements,
    url='https://github.com/deanpienaar/stitch-py',
    author='Dean Pienaar',
    license='MIT',
    packages=find_packages(exclude=['tests']),
)
