from setuptools import find_packages, setup


with open('./requirements/base.txt', 'r') as f:
    requirements = f.read().split('\n')


with open('./README.md', 'r') as f:
    readme = f.read()


setup(
    name='stitch_sdk',
    version='v0.1.0',
    description='Unofficial Stitch Python SDK',
    long_description=readme,
    install_requires=requirements,
    url='https://github.com/deanpienaar/stitch-py',
    author='Dean Pienaar',
    license='MIT',
    packages=find_packages(exclude=['tests']),
)
