from ConfigParser import ConfigParser
import os.path
import sys

# Parse the configuration file for a valid blueprint-io server. 

cfg = ConfigParser(defaults={'server': 'http://127.0.0.1:5000'})

cfg.read(['/etc/blueprint-io.cfg',
          os.path.expanduser('~/.blueprint-io.cfg')])

for option in ('server',):
    if not cfg.has_option('DEFAULT', option):
        sys.stderr.write('cfg: missing {0}\n'.format(option))
        sys.exit(1)

def server():
    """
    Return the configured blueprint-io server or default.
    """
    return cfg.get('DEFAULT', 'server')
