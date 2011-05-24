import json
import requests

default_url = "http://127.0.0.1:5000/"

def pull():
    """docstring for pull"""
    pass

def push(b):
    """
    Push a blueprint to server specified in /etc/blueprint-io-server.cfg,
    ~/.blueprint-io-server.cfg or default to http://blueprint.devstructure.com
    """
    
    """
    GET /secret
    Create a new secret key known only to the caller. This is the namespace beneath which the caller’s blueprints are stored.
    
    Responses:
    201: success; the body contains a new 64-byte secret key.
    502: failure; the upstream storage service failed.
    """
    # TODO: check for local config
    
    r = requests.get(default_url + "secret")
    if r.status_code == 201:
        secret = r.content.rstrip()
        print "SECRET: %s \n" % secret
    elif r.status_code == 502:
      print '502: GET failure; the upstream storage service failed'
      return
     else:
        print 'GET failure'
        return
   
    """
    PUT /secret/name
    Store the JSON representation of the blueprint name. The Content-Type of the body must be application/json.

    Parameters:
    secret: a 64-byte identifier containing numbers, letters, underscores, and dashes.
    name: a blueprint name; it may not contain whitespace or / characters.

    Responses:
    202: success; the blueprint was well-formed and stored; the body contains pre-signed URIs for uploading source tarballs.
    400: failure; the blueprint was not well-formed.
    502: failure; the upstream storage service failed.
    """

    secret_url = default_url + secret + '/' + b.name
    
    r = requests.put(secret_url, files = b)
    if r.status_code == 202:
        pass
    elif r.status_code == 400:
        print '400: PUT failure; the blueprint was not well-formed'
        return
    elif r.status_code == 502:
        print '502: json PUT failure; the upstream storage service failed'
        return
    else:
        print 'json PUT failure'
        return
    

    """
    PUT /secret/name/sha.tar
    Store a source tarball referenced by blueprint name. The Content-Type of the body must be application/x-tar.

    Parameters:
    secret: a 64-byte identifier containing numbers, letters, underscores, and dashes.
    name: a blueprint name; it may not contain whitespace or / characters.
    sha: a 40-byte hexadecimal representation of a SHA1 sum.

    Responses:
    202: success; the tarball was stored.
    400: failure; the SHA1 sum of the body did not match sha.
    404: failure; the secret or blueprint name was not found.
    502: failure; the upstream storage service failed.
    """
    
    tree = git.tree(b._commit)
    for dirname, filename in sorted(b.sources.iteritems()):
        blob = git.blob(tree, filename)
        content = git.content(blob)
    
    content_type = {'content-type': 'application/x-tar'}
    r = requests.put(secret_url + '/' + content, headers=content_type, files=content )
    if r.status_code == 202:
        print 'SUCCESS: your blueprint was stored and can be retrieved from %s' % secret_url
    elif r.status_code == 400:
        print '400: tarball PUT failure; the SHA1 sum of the body did not match sha'
    elif r.status_code == 404:
        print '404: tarball PUT failure; the secret or blueprint name was not found'
    elif r.status_code == 502:
        print '502: tarball PUT failurel the upstream storage service failed'
    else:
        print 'tarball PUT failure'
    
    return
    