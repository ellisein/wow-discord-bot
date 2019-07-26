import os
import json
from configparser import RawConfigParser


_CONFIG_DATA = dict()

def read_cfg(filename):
    if not os.path.isfile(filename):
        return False

    config = RawConfigParser()
    config.read(filename)

    for s in config.sections():
        for i in config.items(s):
            _CONFIG_DATA["{}_{}".format(s, i[0])] = i[1]
    return True

def read_json(filename):
    if not os.path.isfile(filename):
        return False

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    for d in data:
        _CONFIG_DATA[d] = data[d]
    return True

def read_config(filename):
    ret = False
    if filename.endswith(".cfg"):
        ret = read_cfg(filename)
    elif filename.endswith(".json"):
        ret = read_json(filename)

    if ret:
        print("Successfully read config file from '{}'.".format(filename))
    else:
        print("Cannot read config file '{}'.".format(filename))

def get(label):
    if label in _CONFIG_DATA:
        return _CONFIG_DATA[label]
    print("Cannot find config value '{}'.".format(label))
    return None

read_config("key.cfg")
read_config("settings.cfg")
read_config("params.json")
