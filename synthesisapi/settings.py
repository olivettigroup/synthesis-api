from schemas import (target_entity)
from os import (environ)

MONGO_URI = environ.get('MONGOLAB_URI')
MONGO_PORT = int(environ.get('PORT', 5000))

PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

DOMAIN = {
  'materials': target_entity
}

