#!/usr/bin/env python

from distutils.core import setup
from os import path
from password_generator import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Password Generator',
    version=__version__,
    description='A program that generates passwords and store their '
    'parameters locally.',
    author='Marcelo Lacerda',
    author_email='marceloslacerda@gmail.com',
    url='https://github.com/marceloslacerda/password_generator',
    entry_points={
        'console_scripts': [
            'password-generator = password_generator:main',
        ],
      },
    packages=['password_generator'],
    long_description=long_description,
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Encryption :: Password Manager',
        'License :: BSD',
        'Programming Language :: Python :: 3.4',
    ],
      keywords='password encryption',
    install_requires=['tldextract==2.0.1', 'docopt==0.6.2', 'yesno==0.0.0'],
)
