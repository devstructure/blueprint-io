import httplib
import urlparse

import cfg


def connect(server):
    if not server:
        server = cfg.server()
    url = urlparse.urlparse(server)
    if -1 == url.netloc.find(':'):
        port = url.port or 443 if 'https' == url.scheme else 80
    else:
        port = None
    if 'https' == url.scheme:
        return httplib.HTTPSConnection(url.netloc, port)
    else:
        return httplib.HTTPConnection(url.netloc, port)


def get(path, headers={}, server=None):
    c = connect(server)
    c.request('GET', path, None, headers)
    r = c.getresponse()
    # Handle redirects
    while r.status in set([301, 302, 307]):
       url = urlparse.urlparse(r.getheader('location'))
       r = get(url.path,
               {'Content-Type': r.getheader('content-type')},
               urlparse.urlunparse((url.scheme, url.netloc, '', '', '', '')))
    return r


def post(path, body, headers={}, server=None):
    c = connect(server)
    c.request('POST', path, body, headers)
    return c.getresponse()


def put(path, body, headers={}, server=None):
    c = connect(server)
    if len(body) > 0:
        c.request('PUT', path, body, headers)
    else:
        c.request('PUT', path, body)
    return c.getresponse()


def delete(path, server=None):
    c = connect(server)
    c.request('DELETE', path)
    return c.getresponse()
