import os
from configparser import RawConfigParser


_CONFIG_DATA = dict()

def read_config(filename):
    if not os.path.isfile(filename):
        print("Cannot find config file '{}'.".format(filename))
        return

    config = RawConfigParser()
    config.read(filename)

    for s in config.sections():
        for i in config.items(s):
            _CONFIG_DATA["{}_{}".format(s, i[0])] = i[1]
    print("Successfully read config file from '{}'.".format(filename))

def get(label):
    if label in _CONFIG_DATA:
        return _CONFIG_DATA[label]
    print("Cannot find config value '{}'.".format(label))
    return None

read_config("key.cfg")
read_config("settings.cfg")
