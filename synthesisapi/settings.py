from schemas import (target_entity)
from os import (environ)

MONGO_URI = environ.get('MONGOLAB_URI')

PUBLIC_METHODS = ['GET', 'POST']
PUBLIC_ITEM_METHODS = ['GET', 'POST']

RESOURCE_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
ITEM_METHODS = ['GET', 'POST', 'PUT', 'DELETE']

DOMAIN = {
  'materials': target_entity
}

