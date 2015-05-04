from mongokit import (Connection, Document)
import bson
import datetime

# Paragraph object
class Paragraph(Document):
    __database__ = 'synthesis-api'  
    __collection__ = 'paragraphs'

    structure = {
        'doi' : unicode,            #doi of article the paragraph belongs to
        'feature_vector': [int],    #calculated feature vector of Paragraph
        'text': unicode,            #stringified version of the paragraph
        'is_recipe': bool           #if it is a recipe
    }

    required_fields = ['doi', 'text']
    default_values = {
        'feature_vector': [],
        'is_recipe': False
    }

# Query object
class Query(Document):
    __database__ = 'synthesis-api'
    __collection__ = 'queries'

    structure = {
        'material_id': unicode, 
        'paragraph': bson.ObjectId, # Holds one paragraph ID
        'rank': int #Holds the rank of the paragraph given the query
    }

    required_fields = ['paragraph']

    default_values = {
        'rank': 0
    }

# Feedback Object
class Feedback(Document):
    __database__ = 'synthesis-api'
    __collection__ = 'feedback'

    structure = {
        'material_id': unicode,     
        'paragraph_id': unicode,
        'user_id': unicode,         #id of the user who gave feedback
        'type': unicode,            #IS_RECIPE or IS_RELATED_RECIPE
        'value': bool,              #answer to the type question
        'date_creation': datetime.datetime
    }

    required_fields = ['material_id', 'paragraph_id', 'user_id', 'type', 'value']
