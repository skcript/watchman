# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='watchman',
    version='0.0.1',
    description='Make data smarter',
    long_description=readme,
    authors=['Swaathi Kakarla', 'Shilpi Agrawal'],
    authors_email=['swaathi@skcript.com', 'shilpi@skcript.com'],
    url='http://www.skcript.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=(
    	['pyyaml'], ['logging'], ['watchdog'], ['observer'], ['requests'])
)
