from setuptools import setup

from os import path
import shutil

if path.isfile('README.md'):
    shutil.copyfile('README.md', 'README')

setup(
    name='ent',
    description='library for creating arbitrary data structures',
    version='0.2.3',
    author='John Reese',
    author_email='john@noswap.com',
    url='https://github.com/jreese/ent',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 3 - Alpha',
    ],
    license='MIT License',
    packages=['ent'],
    requires=['future'],
)
