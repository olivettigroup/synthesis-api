from schemas import (target_entity)

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = ''
MONGO_PASSWORD = ''
MONGO_DBNAME = 'synthapi'

PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

DOMAIN = {
  'materials': target_entity
}

