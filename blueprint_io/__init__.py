import cfg
import json
import logging
import sys
import urlparse

from blueprint import git
from blueprint import Blueprint
from blueprint import context_managers
import http


server = cfg.server()


def pull(secret, name):
    """
    Pull a blueprint from the secret and name on the configured server.
    """

    # GET /secret/name
    # Fetch the JSON representation of the blueprint name.
    # 
    # Parameters:
    # secret: a 64-byte identifier containing numbers, letters, underscores, and dashes.
    # name: a blueprint name; it may not contain whitespace or / characters.
    #
    # GET /secret/name/sha.tar
    # Fetch a source tarball referenced by blueprint name.
    # 
    # Parameters:
    # secret: a 64-byte identifier containing numbers, letters, underscores, and dashes.
    # name: a blueprint name; it may not contain whitespace or / characters.
    # sha: a 40-byte hexadecimal representation of a SHA1 sum.
    r = http.get('/{0}/{1}'.format(secret, name))
    if 200 == r.status:
        b = Blueprint()
        b.name = name
        b.update(json.loads(r.read()))

        for filename in b.sources.itervalues():
            r = http.get('/{0}/{1}/{2}'.format(secret, name, filename))
            if 200 == r.status:
                try:
                    f = open(filename, 'w')
                    f.write(r.read())
                except OSError:
                    logging.error('could not open {0}'.format(filename))
                    return None
                finally:
                    f.close()
            elif 404 == r.status:
                logging.error('{0} not found'.format(filename))
                return None
            elif 502 == r.status:
                logging.error('upstream storage service failed')
                return None
            else:
                logging.error('unexpected {0} fetching tarball'
                              ''.format(r.status))
                return None

        return b
    elif 404 == r.status:
        logging.error('blueprint not found')
    elif 502 == r.status:
        logging.error('upstream storage service failed')
    else:
        logging.error('unexpected {0} fetching blueprint'.format(r.status))
    return None


def push(secret, b):
    """
    Push a blueprint to the secret and its name on the configured server.
    """

    # PUT /secret/name
    #  Store the JSON representation of the blueprint name. The Content-Type of the body must be application/json.
    # 
    #  Parameters:
    #  secret: a 64-byte identifier containing numbers, letters, underscores, and dashes.
    #  name: a blueprint name; it may not contain whitespace or / characters.
    r = http.put('/{0}/{1}'.format(secret, b.name),
                 b.dumps(),
                 {'Content-Type': 'application/json'})
    if 202 == r.status:
        pass
    elif 400 == r.status:
        logging.error('malformed blueprint')
        return None
    elif 502 ==  r.status:
        logging.error('upstream storage service failed')
        return None
    else:
        logging.error('unexpected {0} storing blueprint'.format(r.status))
        return None

    # PUT /secret/name/sha.tar
    # Store a source tarball referenced by blueprint name. The Content-Type of the body must be application/x-tar.
    # 
    # Parameters:
    # secret: a 64-byte identifier containing numbers, letters, underscores, and dashes.
    # name: a blueprint name; it may not contain whitespace or / characters.
    # sha: a 40-byte hexadecimal representation of a SHA1 sum.
    tree = git.tree(b._commit)
    for dirname, filename in sorted(b.sources.iteritems()):
        blob = git.blob(tree, filename)
        content = git.content(blob)
        r = http.put('/{0}/{1}/{2}'.format(secret, b.name, filename),
                     content,
                     {'Content-Type': 'application/x-tar'})
        if 202 == r.status:
            pass
        elif 400 == r.status:
            logging.error('tarball content or name not expected')
            return None
        elif 404 == r.status:
            logging.error('blueprint not found')
            return None
        elif 502 == r.status:
            logging.error('upstream storage service failed')
            return None
        else:
            logging.error('unexpected {0} storing tarball'.format(r.status))
            return None

    return '{0}/{1}/{2}'.format(server, secret, b.name)


def secret():
    """
    Fetch a new secret from the configured server.
    """
    r = http.get('/secret')
    if 201 == r.status:
        secret = r.read().rstrip()
        logging.warning('created secret {0}'.format(secret))
        logging.warning('store it in ~/.blueprint-io.cfg:')
        sys.stderr.write('\n[default]\nsecret = {0}\nserver = {1}\n\n'.
            format(secret, cfg.server()))
        return secret
    elif 502 == r.status:
        logging.error('upstream storage service failed')
        return None
    else:
        logging.error('unexpected {0} creating secret'.format(r.status))
        return None
