import cfg
import json
import logging
import urlparse

import http

from blueprint import git
from blueprint import Blueprint
from blueprint import context_managers

server = cfg.server()

def pull(url):
    """
    Pull a blueprint from the specified URL
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

    pieces = urlparse.urlparse(url)
    server = pieces.netloc
    url = pieces.path

    with context_managers.mkdtemp():
        r = http.get(url, {}, server)
        logging.info("Connected to blueprint-io server at %s" % server)
        if r.status == 200:
            b = Blueprint()
            b.name = name = pieces.path.rpartition('/')[2]
            b.update(json.loads(r.read()))
            logging.info("Blueprint json pulled, checking for tarballs")

            for filename in b.sources.itervalues():
                logging.info("Downloading %s, this might take a while" % filename)
                r = http.get(url + '/' + filename, {}, server)

                if r.status == 200:
                    try:
                        tarfile = open(filename, 'w')
                        tarfile.write(r.read())
                        logging.info("Blueprint tarballs pulled")
                    except OSError:
                        return
                    finally:
                        tarfile.close()

                elif r.status == 404:
                    logging.error("[404] The sha tarball was not found")
                    return

                elif r.status == 502:
                    logging.error("[502] The upstream storage service failed and the blueprint was not pulled")
                    return

                else:
                    logging.error("[%s] GET error retreiving blueprint files" % r.status)
                    return
            
            logging.info('Storing blueprint on this machine')
            b.commit('')
            logging.info('Success! Blueprint pulled and is ready for use.')

        elif r.status == 404:
            logging.error("[404] A blueprint could not be pulled from %s" % pieces.netloc + pieces.path)
            return

        else:
            logging.error("[%s] GET error" % r.status)
            return

    return


def push(b):
    """
    Push a blueprint to server specified in /etc/blueprint-io.cfg,
    ~/.blueprint-io.cfg or default to https://devstructure.com
    """

    # GET /secret
    # Create a new secret key known only to the caller. 
	# This is the namespace beneath which the caller’s blueprints are stored.
    
    r = http.get("/secret")
    logging.info("Connected to blueprint-io server at %s" % server)
    if r.status == 201:
        secret = r.read().rstrip()
        logging.info("Secret key: %s" % secret)
    elif r.status == 502:
        logging.error('[502] GET failure; the upstream storage service failed')
        return
    else:
        logging.error('[%s] GET failure' % r.status)
        return
   
    # PUT /secret/name
    #  Store the JSON representation of the blueprint name. The Content-Type of the body must be application/json.
    # 
    #  Parameters:
    #  secret: a 64-byte identifier containing numbers, letters, underscores, and dashes.
    #  name: a blueprint name; it may not contain whitespace or / characters.
    
    r = http.put(
        url = '/' + secret + '/' + b.name,
        body = b.dumps(),
        headers = {'Content-type': 'application/json'} )

    if r.status == 202:
        logging.info('Blueprint JSON stored on server, moving on to the blueprint tarballs')
    elif r.status == 400:
        logging.error('[400] PUT failure; the blueprint was not well-formed')
        return
    elif r.status == 502:
        logging.error('[502] JSON PUT failure; the upstream storage service failed')
        return
    else:
        logging.error('[%s] JSON PUT failure' % r.status)
        return
    

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
        logging.info("Uploading %s, this might take a while" % filename)
        r = http.put(
            url = '/' + secret + '/' + b.name + '/' + filename,
            body = content,
            headers = {'Content-type': 'application/x-tar'})

    if r.status == 202:
        logging.info('Success! Blueprint pushed and available at: %s' % server + '/' + secret + '/' + b.name)
    elif r.status == 400:
        logging.error('[400] tarball PUT failure; the SHA1 sum of the body did not match sha')
    elif r.status == 404:
        logging.error('[404] tarball PUT failure; the secret or blueprint name was not found')
    elif r.status == 502:
        logging.error('[502] tarball PUT failurel the upstream storage service failed')
    else:
        logging.error('[%s] tarball PUT failure' % r.status)
    
    return
    