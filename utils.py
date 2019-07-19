from urllib import parse

import config


def encode(base, url):
    parsed = parse.urlparse(url)
    parsed = parse.parse_qs(parsed.query)
    encoded = "{}?{}".format(base, parse.urlencode(parsed, doseq=True))
    return encoded

def parse_character_name(arg):
    cnt = arg.count("-")
    if cnt < 1:
        return arg, config.get("default_server")
    elif cnt == 1:
        return arg.split("-")
    else:
        return parse_character_name(arg.split("-")[0])
