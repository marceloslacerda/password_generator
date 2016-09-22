import collections
import hashlib
import itertools
import logging
import os.path
import shelve
import tldextract

INFO_PATH = os.path.expanduser('~/.pinfo')
ALGORITHM = 'sha256'
PASSES = 150000

PassInfo = collections.namedtuple('PassInfo', ['salt', 'length', 'symbols', 'id'])
ALPHANUM = bytearray(itertools.chain(range(48, 58), range(65, 91),
                                     range(97, 123)))


def translate(bytes_array, length, symbols):
    table = ALPHANUM[:]
    table.extend(bytearray(symbols, 'utf-8'))
    pass_ = str(bytes(ALPHANUM[b % len(ALPHANUM)] for b in bytes_array), 'utf-8')
    return pass_[:length - len(symbols)] + symbols


def gen_msg(hostname, pass_, usr):
    return bytearray(hostname + pass_ + usr, 'utf-8')


def get_pinfo_key(user, hostname):
    return hostname + user


def get_pinfo(db, user, hostname):
    try:
        return db[get_pinfo_key(user, hostname)]
    except KeyError:
        pass


def store_pinfo(db, hostname, user, pinfo):
    db[get_pinfo_key(user, hostname)] = pinfo


def get_db():
    try:
        return shelve.open(INFO_PATH, writeback=True)
    except IOError:
        raise IOError('Could not open the password info file. Please check your '
                      'permissions and try again.')


def get_hostname(url):
    if not url:
        url = input('URL: ').strip()
    o = tldextract.extract(url)
    hostname = o.domain + '.' + o.suffix
    logging.info('Hostname, %s', hostname)
    return hostname


def get_password(hostname, pass_, pinfo):
    msg = gen_msg(hostname, pass_, pinfo.id)
    derived_key = hashlib.pbkdf2_hmac(ALGORITHM, msg, pinfo.salt, PASSES)
    password = translate(derived_key, pinfo.length, pinfo.symbols)
    return password
