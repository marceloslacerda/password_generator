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
import yesno

from .password import (get_db, get_hostname, get_pinfo, get_pinfo_key,
                       store_pinfo, get_password, PassInfo)

DEFAULT_USER = os.environ['USER']
DEFAULT_LENGTH = 16


def print_password(user, hostname):
    pinfo = get_pinfo(get_db(), user, hostname)
    if pinfo is None:
        print('Password not found')
        return
    pass_ = getpass.getpass('Master key: ')
    password = get_password(hostname, pass_, pinfo)
    print('Password: ', password)


def rm_pinfo(user, hostname):
    db = get_db()
    if get_pinfo(db, user, hostname):
        del db[get_pinfo_key(user, hostname)]
        logging.info('Removed password successfully')
    else:
        logging.error('No entry for user %s, hostname %s found.', user, hostname)
        exit(1)


def list_pinfo(user):
    db = get_db()
    for key in db:
        if user in key:
            print(key.split(user)[0])


def set_password(user, hostname, length, symbols):
    db = get_db()
    pinfo = get_pinfo(get_db(), user, hostname)
    if pinfo is not None:
        if not yesno.input_until_bool('Password already exists, do you wish to continue'):
            exit(0)
    salt = os.urandom(32)
    pinfo = PassInfo(salt, length, symbols, user)
    pass_ = getpass.getpass('Master key: ')
    password = get_password(hostname, pass_, pinfo)
    print('Password: ', password)
    if yesno.input_until_bool('Save password info'):
        store_pinfo(db, hostname, user, pinfo)


def get_length(length):
    return DEFAULT_LENGTH if not length else int(length)


def get_symbols(symbols):
    return '' if not symbols else symbols


def main():
    arguments = docopt.docopt(__doc__, version='Password Generator 0.0.0')
    logging.basicConfig(format='%(levelname)s: %(message)s', level='INFO')
    if arguments['--user']:
        user = arguments['--user']
    else:
        user = DEFAULT_USER
    logging.info('User, %s', user)
    try:
        if arguments['list']:
            list_pinfo(user)
        elif arguments['get']:
            print_password(user, get_hostname(arguments['--url']))
        elif arguments['set']:
            set_password(user, get_hostname(arguments['--url']),
                         get_length(arguments['--length']),
                         get_symbols(arguments['--symbols']))
        elif arguments['rm']:
            rm_pinfo(user, get_hostname(arguments['--url']))
    except IOError as e:
        logging.error(str(e))
        exit(1)
