from schemas import (material)
from os import (environ)

MONGO_URI = environ.get('MONGOLAB_URI')

PUBLIC_METHODS = ['GET', 'PUT']
PUBLIC_ITEM_METHODS = ['GET', 'PUT']

RESOURCE_METHODS = ['GET', 'PUT']
ITEM_METHODS = ['GET', 'PUT']

DOMAIN = {
  'materials': material
}
