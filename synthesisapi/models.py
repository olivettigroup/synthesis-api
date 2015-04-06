from mongokit import (Connection, Document)

# Paragraph object

class Paragraph(Document):
    __database__ = 'synthesis-api'  # TODO
    __collection__ = 'paragraphs'

    structure = {
        'doi' : unicode, #doi of article the paragraph belongs to
        'feature_vector': [int], #calculated feature vector of Paragraph
        'text': unicode, #stringified version of the paragraph
        'is_recipe': bool #if it is a recipe
    }

    required_fields = ['doi', 'text']
    default_values = {
        'feature_vector': [],
        'is_recipe': False
    }

# TODO: should we store Paper objects?

# Query object

class Query(Document):
    _database__ = 'synthesis-api'
    __collection__ = 'queries'

    structure = {
        # key: material_id
        # list of associated paragraphs
    }

    required_fields = []

    default_values = {}


