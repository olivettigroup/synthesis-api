from eve import Eve
from os import (environ)

# Heroku support: bind to PORT if defined, otherwise default to 5000.
if 'PORT' in environ:
    port = int(environ.get('PORT'))
    host = '0.0.0.0'
else:
    port = 5000
    host = '127.0.0.1'

app = Eve()

if __name__ == '__main__':
    app.run(host=host, port=port)