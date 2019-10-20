# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='LandrayTest',
    version='0.1.0',
    description='易企签 接口演示程序',
    long_description=readme,
    author='Jess',
    author_email='2482003411@qq.com',
    url='https://github.com/JessKXWL/LandrayTest',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

