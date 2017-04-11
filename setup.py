import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as required_file:
    required = required_file.read().splitlines()

setup(
    name='poolhub',
    version='0.0.9',
    packages=find_packages(),
    description="Track threads in your Python program.",
    author='Paul Litvak',
    author_email='litvakpol@012.net.il',
    install_requires=required,
    include_package_data=True,
    url='https://github.com/tsarpaul/poolhub',
    license='MIT License',
    keywords=['multithreading', 'python', 'tool'],
    classifiers=[
    ],
)
