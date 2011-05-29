import requests
import logging
import cfg
server = cfg.server()

def pull():
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
    # Responses:
    # 200: success; the body contains the JSON representation of the blueprint name.
    # 404: failure; the secret or blueprint name was not found.
    # 
    # 
    # GET /secret/name/sha.tar
    # Fetch a source tarball referenced by blueprint name.
    # 
    # Parameters:
    # secret: a 64-byte identifier containing numbers, letters, underscores, and dashes.
    # name: a blueprint name; it may not contain whitespace or / characters.
    # sha: a 40-byte hexadecimal representation of a SHA1 sum.
    # 
    # Responses:
    # 200: success; the body contains the application/x-tar content of the source tarball.
    # 404: failure; the secret, blueprint name, or sha was not found.
    # 502: failure; the upstream storage service failed.
    
    
    pass

def push(b):
    """
    Push a blueprint to server specified in /etc/blueprint-io-server.cfg,
    ~/.blueprint-io.cfg or default to https://devstructure.com
    """
    
    # GET /secret
    # Create a new secret key known only to the caller. 
	# This is the namespace beneath which the caller’s blueprints are stored.
    
    r = requests.get(server + "/secret")
    if r.status_code == 201:
        secret = r.content.rstrip()
        logging.info("SECRET KEY: %s \n" % secret)
    elif r.status_code == 502:
        logging.error('502: GET failure; the upstream storage service failed')
        return
    else:
        logging.error('GET failure')
        return
   
    # PUT /secret/name
    #  Store the JSON representation of the blueprint name. The Content-Type of the body must be application/json.
    # 
    #  Parameters:
    #  secret: a 64-byte identifier containing numbers, letters, underscores, and dashes.
    #  name: a blueprint name; it may not contain whitespace or / characters.

 
    secret_url = server + '/' + secret + '/' + b.name
    content_type = {'Content-type': 'application/json'}

    
    r = requests.put(secret_url, headers = content_type, data = b)
    if r.status_code == 202:
        logging.info('Your blueprint JSON was stored on server, moving on to the blueprint files')
    elif r.status_code == 400:
        logging.error('400: PUT failure; the blueprint was not well-formed')
        return
    elif r.status_code == 502:
        logging.error('502: json PUT failure; the upstream storage service failed')
        return
    else:
        logging.error('json PUT failure')
        return
    

    # PUT /secret/name/sha.tar
    # Store a source tarball referenced by blueprint name. The Content-Type of the body must be application/x-tar.
    # 
    # Parameters:
    # secret: a 64-byte identifier containing numbers, letters, underscores, and dashes.
    # name: a blueprint name; it may not contain whitespace or / characters.
    # sha: a 40-byte hexadecimal representation of a SHA1 sum.

    # FIXME: not working
    tree = git.tree(b._commit)
    for dirname, filename in sorted(b.sources.iteritems()):
        blob = git.blob(tree, filename)
        content = git.content(blob)
    
    content_type = {'Content-type': 'application/x-tar'}
    r = requests.put(secret_url + '/' + content, headers=content_type, files=content )
    if r.status_code == 202:
        logging.info('Your server blueprint was saved and can be retrieved from %s' % secret_url)
    elif r.status_code == 400:
        logging.error('400: tarball PUT failure; the SHA1 sum of the body did not match sha')
    elif r.status_code == 404:
        logging.error('404: tarball PUT failure; the secret or blueprint name was not found')
    elif r.status_code == 502:
        logging.error('502: tarball PUT failurel the upstream storage service failed')
    else:
        logging.error('tarball PUT failure')
    
    return
    