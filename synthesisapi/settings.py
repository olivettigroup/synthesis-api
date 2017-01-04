from schemas import (material)
from os import (environ)

MONGO_URI = environ.get('MONGOLAB_URI')

PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PUT', 'DELETE']

DOMAIN = {
  'materials': material
}
