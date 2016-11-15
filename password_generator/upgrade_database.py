#!/usr/bin/env python3

import collections, shelve, sys, base64, json

PassInfo = collections.namedtuple('PassInfo', ['salt', 'length', 'symbols', 'id'])

def list_pinfo():
    path = sys.argv[1]
    db = get_db(path)
    def aux():
        for key in db:
            try:
                entry = db[key]
            except AttributeError as err:
                print('Could not retrieve data for password entry: ', key, file=sys.stderr)
                continue
            yield key, pinfo_to_json(entry)
    print(json.dumps(dict(aux()))) 


def pinfo_to_json(pinfo):
    print(dir(pinfo))
    return {
        'length': pinfo.length,
        'symbols': pinfo.symbols,
        'id' : pinfo.id,
        'salt' : base64.b64encode(pinfo.salt).decode('utf-8')
    }

def get_db(path):
    try:
        return shelve.open(path)
    except IOError:
        print('Could not open the password info file. Please check your '
                      'permissions and try again.')
        exit(1)

if __name__ == '__main__':
    list_pinfo()
