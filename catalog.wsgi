import logging, sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/catalog')
from application import app as application
application.secret_key = 'cgvSdvbFudzOunQFaklmHA=='
