#!/usr/bin/python3

"""Password Generator

Usage:
  password_generator get [-U <usr> | --user=<usr>] [-u <url> | --url=<url>] [-n] [--db <database>] --debug <password>
  password_generator set [-U <usr> | --user=<usr>] [-u <url> | --url=<url>] [-n] [--length=<length>] [--symbols=<symbols>] [--db <database>] --debug <password>
  password_generator list [-U <usr> | --user=<usr>] [--db <database>]
  password_generator rm [-U --user=<usr>] [-u <url> | --url=<url>] [-n] [--db <database>]


Options:
  -U <usr>, --user=<usr> The username associated with that password
  -u <url>, --url=<url>  The url that uses that password. It will be stripped of subdomains and trailing parameters. Use -n to disable this behaviour
  -n                     Use this when you want to use the url as it is
  --length=<length>      The length of the password
  --symbols=<symbols>    Extra symbols to be appended to the password
  --db=<database>        Relative path to a json file with the password database
  --debug=<password>     Read the password from argument !!DO NOT USE!!
"""

import docopt
import logging
import os
import conz
import pyperclip
import daemon
import time

from getpass import getpass

from .password import *
from . import __version__

DEFAULT_USER = os.environ['USER']
DEFAULT_LENGTH = 16
TIME_BEFORE_CLEAN = 10
MAX_VERSION = 1
cn = conz.Console()
debug = False


def print_password(password, callback=None):
    try:
        if debug:
            raise pyperclip.exceptions.PyperclipException()
        pyperclip.copy(password)
        if len(password) > 10:
            print('Password ' + password[:3] + '... copied to clipboard')
        else:
            print('Password ' + password[0] + '... copied to clipboard')
        print('The password will be removed from'
              ' clipboard after {} seconds'.format(TIME_BEFORE_CLEAN))
        if callback is not None:
            callback()
        with daemon.DaemonContext():
            time.sleep(TIME_BEFORE_CLEAN)
            if pyperclip.paste() == password:
                pyperclip.copy('')
    except pyperclip.exceptions.PyperclipException:
        logging.warning('Could not copy to clipboard, please install either '
                        'xclip or xsel to use that feature.')
        print('Password: ', password)
        if callback is not None:
            callback()


def print_password_cmd(user, hostname, db_path):
    try:
        pinfo = get_pinfo(get_db(db_path), user, hostname)
    except KeyError:
        print('Password not found')
        exit(1)
    pass_ = getpass('Master key: ')
    password = get_password(hostname, pass_, pinfo)
    print_password(password)

def set_password(user, hostname, length, symbols, db_path):
    db = get_db(db_path)
    try:
        pinfo = get_pinfo(db, user, hostname)
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
        'id': user,
        'version': MAX_VERSION
    }
    pass_ = getpass('Master key: ')
    password = get_password(hostname, pass_, pinfo)
    def save_password_callback():
        if cn.yesno('Save password info'):
            store_pinfo(db, hostname, user, pinfo, db_path)
    print_password(password, save_password_callback)

def rm_password(user, hostname, db_path):
    db = get_db(db_path)
    try:
        rm_pinfo(db, user, hostname, db_path)
        logging.info('Removed password successfully')
    except KeyError:
        print('Password not found')
        exit(1)

def list_hostnames(user, db_path):
    db = get_db(db_path)
    pinfos = list_pinfo(db, user)
    if len(pinfos) == 0:
        print('No entries found in the database')
    else:
        for host in pinfos:
            print(host)


def get_length(length):
    return DEFAULT_LENGTH if not length else int(length)


def get_symbols(symbols):
    return '' if not symbols else symbols


def get_hostname(url, noextract):
    if not url:
        url = input('URL: ').strip()
    if not noextract:
        import tldextract # here because it can be slow to load
        o = tldextract.extract(url)
        hostname = o.domain + '.' + o.suffix
        return hostname
    else:
        return url


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

    if arguments['--debug']:
        global getpass
        getpass = lambda x: arguments['--debug']
        global debug
        debug = True

    logging.info('User, %s', user)
    if arguments['list']:
        pass
    else:
        hostname = get_hostname(arguments['--url'], arguments['-n'])
        logging.info('Hostname, %s', hostname)
    try:
        if arguments['list']:
            list_hostnames(user, arguments['--db'])
        elif arguments['get']:
            print_password_cmd(user, hostname, arguments['--db'])
        elif arguments['set']:
            set_password(user, hostname,
                         get_length(arguments['--length']),
                         get_symbols(arguments['--symbols']),
                         arguments['--db']
            )
        elif arguments['rm']:
            rm_password(user, hostname, arguments['--db'])
    except IOError as e:
        logging.error(str(e))
        exit(1)
