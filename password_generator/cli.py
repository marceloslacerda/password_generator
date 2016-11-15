#!/usr/bin/python3

"""Password Generator

Usage:
  password_generator get [--user=<usr>] [--url=<url>]
  password_generator set [--user=<usr>] [--url=<url>] [--length=<length>] [--symbols=<symbols>]
  password_generator list [--user=<usr>]
  password_generator rm [--user=<usr>] [--url=<url>]
"""

import docopt
import getpass
import logging
import os
import conz


from .password import *
from . import __version__

DEFAULT_USER = os.environ['USER']
DEFAULT_LENGTH = 16
cn = conz.Console()


def print_password(user, hostname):
    try:
        pinfo = get_pinfo(get_db(), user, hostname)
    except KeyError:
        print('Password not found')
        exit(1)
    pass_ = getpass.getpass('Master key: ')
    password = get_password(hostname, pass_, pinfo)
    print('Password: ', password)


def set_password(user, hostname, length, symbols):
    db = get_db()
    try:
        pinfo = get_pinfo(get_db(), user, hostname)
        if not cn.yesno('Password already exists, do you wish to continue?'):
            exit(0)
    except KeyError:
        pass
    salt = os.urandom(32)
    pinfo = {
        'salt': salt,
        'length': length,
        'symbols': symbols,
        'hostname': hostname, # watch out, old databases didn't store hostname
        'id': user
    }
    pass_ = getpass.getpass('Master key: ')
    password = get_password(hostname, pass_, pinfo)
    print('Password: ', password)
    if cn.yesno('Save password info'):
        store_pinfo(db, hostname, user, pinfo)

def rm_password(user, hostname):
    db = get_db()
    try:
        rm_pinfo(db, user, hostname)
        logging.info('Removed password successfully')
    except KeyError:
        print('Password not found')
        exit(1)

def list_hostnames(user):
    db = get_db()
    for host in list_pinfo(db, user):
        print(host)


def get_length(length):
    return DEFAULT_LENGTH if not length else int(length)


def get_symbols(symbols):
    return '' if not symbols else symbols


def main():
    arguments = docopt.docopt(
        __doc__,
        version='Password Generator ' + __version__
    )
    logging.basicConfig(format='%(levelname)s: %(message)s', level='INFO')
    if arguments['--user']:
        user = arguments['--user']
    else:
        user = DEFAULT_USER
    logging.info('User, %s', user)
    try:
        if arguments['list']:
            list_hostnames(user)
        elif arguments['get']:
            print_password(user, get_hostname(arguments['--url']))
        elif arguments['set']:
            set_password(user, get_hostname(arguments['--url']),
                         get_length(arguments['--length']),
                         get_symbols(arguments['--symbols']))
        elif arguments['rm']:
            rm_password(user, get_hostname(arguments['--url']))
    except IOError as e:
        logging.error(str(e))
        exit(1)
