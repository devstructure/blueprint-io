import httplib

import cfg

server = cfg.server()

# FIXME: fix server configs to handle port
def connect():
    return httplib.HTTPConnection("127.0.0.1", "5000")

def get(url, headers={}):
    c = connect()
    c.request("GET", url, None, headers)
    return c.getresponse()

def post(url, body, headers={}):
    c = connect()
    c.request('POST', url, body, headers)
    return c.getresponse()

def put(url, body, headers={}):
    c = connect()
    if len(body) > 0:
        c.request("PUT", url, body, headers)
    else:
        c.request("PUT", url, body)
    return c.getresponse()

def delete(url):
    c = connect()
    c.request("DELETE", url)
    return c.getresponse()
