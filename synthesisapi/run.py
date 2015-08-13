from eve import Eve
from os import (environ)

e = Eve()

def app():
  e.run(port=int(environ.get('PORT', 5000)))

if __name__ == '__main__':
  app()