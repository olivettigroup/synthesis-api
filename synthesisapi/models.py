from mongokit import (Connection, Document)
import bson
import datetime

# Paragraph object
class Paragraph(Document):
  '''
  Models a paragraph belonging to an article
  '''

  __database__ = 'predsynth'
  __collection__ = 'paragraphs'

  structure = {
    'doi' : unicode, #doi of article the paragraph belongs to
    'order': int, #which paragraph in the paper (i.e. sequence); 0-indexed
    'parse_tree_id': unicode, #Map to parse tree of this paragraph
    'feature_vector': [int], #calculated feature vector of Paragraph
    'text': unicode, #stringified version of the paragraph
    'is_recipe': bool #if it is a recipe
  }

  required_fields = ['doi', 'text']
  default_values = {
    'feature_vector': [],
    'is_recipe': False
  }

# Query object
class Query(Document):
  '''
  Models a query made to the API server 
  '''
  __database__ = 'synthesis-api'
  __collection__ = 'queries'

  structure = {
    'material_id': unicode, 
    'paragraph': bson.ObjectId, # Holds one paragraph ID
    'rank': int #Holds the relevance rank of the paragraph given the query (i.e. return order of paragraphs)
  }

  required_fields = ['paragraph']

  default_values = {
    'rank': 0
  }

# Feedback Object
class Feedback(Document):
  '''
  Models feedback given to the API server (for updating paragraph labels)
  '''
  __database__ = 'synthesis-api'
  __collection__ = 'feedback'

  structure = {
    'material_id': unicode,     
    'paragraph_id': unicode,
    'user_id': unicode,         #id of the user who gave feedback
    'type': unicode,            #IS_RECIPE or IS_RELATED_RECIPE
    'value': int,              #answer to the type question (-1 = False, 1 = True)
    'date_creation': datetime.datetime
  }

  required_fields = ['material_id', 'paragraph_id', 'user_id', 'type', 'value']
