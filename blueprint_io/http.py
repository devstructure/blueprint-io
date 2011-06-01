import httplib
import urlparse

import cfg


# FIXME: fix server configs to handle port
def connect(server):
    if not server:
        server = urlparse.urlparse(cfg.server()).netloc
    return httplib.HTTPConnection(server)

def get(url, headers={}, server=None):
    c = connect(server)
    c.request("GET", url, None, headers)
    r = c.getresponse()
    # handle redirects
    while r.status in set([301, 302, 307]):
       pieces = urlparse.urlparse(r.getheader('location'))
       headers = {'Content-type': r.getheader('content-type')}
       r = get(pieces.path, headers, pieces.netloc)
    return r

def post(url, body, headers={}, server=None):
    c = connect(server)
    c.request('POST', url, body, headers)
    return c.getresponse()

def put(url, body, headers={}, server=None):
    c = connect(server)
    if len(body) > 0:
        c.request("PUT", url, body, headers)
    else:
        c.request("PUT", url, body)
    return c.getresponse()

def delete(url, server=None):
    c = connect(server)
    c.request("DELETE", url)
    return c.getresponse()
