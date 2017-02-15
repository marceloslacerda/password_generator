import hashlib
import itertools
import json
import base64
import os
import os.path

INFO_PATH = os.path.expanduser('~/.pinfo.json')
ALGORITHM = 'sha256'
PASSES = 150000
MAX_VERSION = 1

ALPHANUM = bytearray(itertools.chain(range(48, 58), range(65, 91),
                                     range(97, 123)))


def translate(bytes_array, length, symbols):
    table = ALPHANUM[:]
    table.extend(bytearray(symbols, 'utf-8'))
    pass_ = str(bytes(ALPHANUM[b % len(ALPHANUM)] for b in bytes_array),
                'utf-8')
    return pass_[:length - len(symbols)] + symbols


def gen_msg(hostname, pass_, usr):
    return bytearray(hostname + pass_ + usr, 'utf-8')


def get_pinfo_key(user, hostname):
    return hostname + user


def list_pinfo(db, user):
    return [key.split(user)[0] for key in db if user in key]


def get_pinfo(db, user, hostname):
    pinfo = db[get_pinfo_key(user, hostname)]
    pinfo['salt'] = base64.b64decode(pinfo['salt'])
    if pinfo.get('version', 0) > MAX_VERSION:
        raise VersionError()
    return pinfo

def rm_pinfo(db, user, hostname, db_path):
    del db[get_pinfo_key(user, hostname)]
    write_db(db, db_path)


def store_pinfo(db, hostname, user, pinfo, db_path):
    pinfo['salt'] = base64.b64encode(pinfo['salt']).decode('utf-8')
    db[get_pinfo_key(user, hostname)] = pinfo
    write_db(db, db_path)


def write_db(db, db_path):
    path = INFO_PATH if db_path is None else os.path.expanduser(db_path)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(db, f)


def get_db(db_path):
    path = INFO_PATH if db_path is None else os.path.expanduser(db_path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return dict()
    except IOError:
        raise IOError('Could not open the password info file. Please check your '
                      'permissions and try again.')


def get_password(hostname, pass_, pinfo):
    msg = gen_msg(hostname, pass_, pinfo['id'])
    derived_key = hashlib.pbkdf2_hmac(ALGORITHM, msg, pinfo['salt'], PASSES)
    password = translate(derived_key, pinfo['length'], pinfo['symbols'])
    return password

class VersionError(Exception):
    pass
