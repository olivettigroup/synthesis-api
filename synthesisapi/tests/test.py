from json import loads
from mongokit import Connection
from synthesisapi.models import (Paragraph, Query, Feedback)
import synthesisapi.helper.paragraph as phelpers
import synthesisapi.helper.feedback as fhelpers
from unittest import TestCase

class ModelTester(TestCase):
  def setUp(self):
    self.paragraph = Paragraph()
    self.query = Query()
    self.feedback = Feedback()

  def test_build(self):
    self.assertTrue(self.paragraph is not None)
    self.assertTrue(self.paragraph.structure is not None)

    self.assertTrue(self.query is not None)
    self.assertTrue(self.query.structure is not None)

    self.assertTrue(self.feedback is not None)
    self.assertTrue(self.feedback.structure is not None)


class ParagraphQueryAddRemoveTester(TestCase):
    def setUp(self):
        # MongoDB Setup
        self.connection = Connection()
        self.connection.register([Paragraph])
        self.connection.register([Query])

        self.pa_collection = self.connection['synthesis-api'].paragraphs
        self.qy_collection = self.connection['synthesis-api'].queries

        # Data setup
        self.material_id_1 = '9999999'
        self.material_id_2 = '1000000'
        self.paragraph_data_1 = {'doi': 1, 
                          'feature_vector': [0,1,0], 
                          'text': u'testing paragraph for article 1',
                          'is_recipe': True}
        self.paragraph_data_2 = {'doi': 2, 
                          'feature_vector': [1,1,1], 
                          'text': u'testing paragraph for article 2',
                          'is_recipe': True}
        self.paragraph_data_3 = {'doi': 3,
                          'feature_vector': [2,2,2], 
                          'text': u'testing paragraph for article 3',
                          'is_recipe': True}
        self.small_data = [(self.material_id_1, self.paragraph_data_1)]
        self.medium_data = [(self.material_id_1, self.paragraph_data_1), (self.material_id_2, self.paragraph_data_2)]
        self.large_data = [(self.material_id_1, self.paragraph_data_1), 
                           (self.material_id_2, self.paragraph_data_2),
                           (self.material_id_1, self.paragraph_data_3)]


    def single(self):
        print "running 1"
        # Adding a paragraph
        phelpers.add_paragraphs(self.connection, self.small_data)

        # Checking that the paragraph object was created
        paragraph_object = self.pa_collection.Paragraph.find_one(self.paragraph_data_1) 
        print "paragraph object", paragraph_object
        print self.pa_collection.count()
        self.assertTrue(self.pa_collection.count() == 1)
        self.assertTrue(paragraph_object is not None)

        # Checking that the query object was created
        self.assertTrue(self.qy_collection.count() == 1)
        query_object = self.qy_collection.Query.find_one({'_id': self.material_id_1})
        print "query object", query_object
        self.assertTrue(query_object is not None)

        # Removing the paragraph
        phelpers.remove_paragraphs(self.connection, self.small_data)

        # Checking that the query object has empty list
        qy_object = self.qy_collection.Query.find_one({'_id': self.material_id_1, 'paragraphs': []})
        print "qy object", qy_object
        self.assertTrue(qy_object is not None )

        # Removing the query
        self.qy_collection.remove({'_id': self.material_id_1})
        self.assertTrue(self.qy_collection.count() == 0)

        # Removing the paragraph
        self.pa_collection.remove(self.paragraph_data_1)
        self.assertTrue(self.pa_collection.count() == 0)

    def multiple(self):
        print "running 2"
        phelpers.add_paragraphs(self.connection, self.medium_data)

        # Checking that the paragraph objects was created
        paragraph_object_1 = self.pa_collection.Paragraph.find_one(self.paragraph_data_1) 
        paragraph_object_2 = self.pa_collection.Paragraph.find_one(self.paragraph_data_2) 
        self.assertTrue(self.pa_collection.count() == 2)
        self.assertTrue(paragraph_object_1 is not None)
        self.assertTrue(paragraph_object_2 is not None)

        # Checking that the query objects was created
        query_object_1 = self.qy_collection.Query.find_one({'_id': self.material_id_1})
        query_object_2 = self.qy_collection.Query.find_one({'_id': self.material_id_2})
        self.assertTrue(self.qy_collection.count() == 2)
        self.assertTrue(query_object_1 is not None)
        self.assertTrue(query_object_2 is not None)

        # Printing
        print "Paragraph object 1", paragraph_object_1
        print "Paragraph object 2", paragraph_object_2
        print "Query object 1", query_object_1
        print "Query object 2", query_object_2
        
        # Removing the paragraph
        phelpers.remove_paragraphs(self.connection, self.medium_data)

        # Checking that the query object has empty list
        qy_object_1 = self.qy_collection.Query.find_one({'_id': self.material_id_1, 'paragraphs': []})
        qy_object_2 = self.qy_collection.Query.find_one({'_id': self.material_id_2, 'paragraphs': []})
        self.assertTrue(qy_object_1 is not None )
        self.assertTrue(qy_object_2 is not None )
        print "qy object", qy_object_1
        print "qy object", qy_object_2

        # Removing the query
        self.qy_collection.remove({'_id': self.material_id_1})
        self.qy_collection.remove({'_id': self.material_id_2})
        self.assertTrue(self.qy_collection.count() == 0)

        # Removing the paragraph
        self.pa_collection.remove(self.paragraph_data_1)
        self.pa_collection.remove(self.paragraph_data_2)
        self.assertTrue(self.pa_collection.count() == 0)

    def interleaved_multiple(self):
        print "running 3"
        phelpers.add_paragraphs(self.connection, self.large_data)

        # Checking that the paragraph objects was created
        paragraph_object_1 = self.pa_collection.Paragraph.find_one(self.paragraph_data_1) 
        paragraph_object_2 = self.pa_collection.Paragraph.find_one(self.paragraph_data_2) 
        paragraph_object_3 = self.pa_collection.Paragraph.find_one(self.paragraph_data_3) 
        self.assertTrue(self.pa_collection.count() == 3)
        self.assertTrue(paragraph_object_1 is not None)
        self.assertTrue(paragraph_object_2 is not None)
        self.assertTrue(paragraph_object_3 is not None)

        # Checking that the query objects was created
        query_object_1 = self.qy_collection.Query.find_one({'_id': self.material_id_1})
        query_object_2 = self.qy_collection.Query.find_one({'_id': self.material_id_2})
        self.assertTrue(self.qy_collection.count() == 2)
        self.assertTrue(query_object_1 is not None)
        self.assertTrue(query_object_2 is not None)

        # Printing
        print "Paragraph object 1", paragraph_object_1
        print "Paragraph object 2", paragraph_object_2
        print "Paragraph object 3", paragraph_object_3
        print "Query object 1", query_object_1
        print "Query object 2", query_object_2
        
        # Removing one paragraph
        phelpers.remove_paragraphs(self.connection, self.small_data)

        # Checking that the query object has one less
        qy_object_1 = self.qy_collection.Query.find_one({'_id': self.material_id_2})
        self.assertTrue(len(qy_object_1['paragraphs']) == 1 )
        
        # Removing all paragraphs
        phelpers.remove_paragraphs(self.connection, self.large_data)

        # Checking that the query object has empty list
        qy_object_1 = self.qy_collection.Query.find_one({'_id': self.material_id_2, 'paragraphs': []})
        self.assertTrue(qy_object_1 is not None )
        qy_object_2 = self.qy_collection.Query.find_one({'_id': self.material_id_1, 'paragraphs': []})
        self.assertTrue(qy_object_2 is not None )

        # Removing the query
        self.qy_collection.remove({'_id': self.material_id_1})
        self.qy_collection.remove({'_id': self.material_id_2})
        self.assertTrue(self.qy_collection.count() == 0)

        # Removing the paragraph
        self.pa_collection.remove(self.paragraph_data_1)
        self.pa_collection.remove(self.paragraph_data_2)
        self.pa_collection.remove(self.paragraph_data_3)
        self.assertTrue(self.pa_collection.count() == 0)

    def test_all_possiblitilies(self):
        self.pa_collection.remove(self.paragraph_data_1)
        self.pa_collection.remove(self.paragraph_data_2)
        self.pa_collection.remove(self.paragraph_data_3)
        self.qy_collection.remove({'_id': self.material_id_1})
        self.qy_collection.remove({'_id': self.material_id_2})

        self.single()
        self.multiple()
        self.interleaved_multiple()

        self.pa_collection.remove(self.paragraph_data_1)
        self.pa_collection.remove(self.paragraph_data_2)
        self.pa_collection.remove(self.paragraph_data_3)
        self.qy_collection.remove({'_id': self.material_id_1})
        self.qy_collection.remove({'_id': self.material_id_2})

class ParagraphGetTester(TestCase):
    # TODO: add test case with various queries in db, but getting one
    def setUp(self):
        self.connection = Connection()
        self.connection.register([Paragraph])
        self.connection.register([Query])

        self.pa_collection = self.connection['synthesis-api'].paragraphs
        self.qy_collection = self.connection['synthesis-api'].queries

        self.material_id_1 = '9999999'
        self.paragraph_data_1 = {'doi': 1, 
                          'feature_vector': [0,1,0], 
                          'text': u'testing paragraph for article 1',
                          'is_recipe': True}
        self.paragraph_data_2 = {'doi': 2, 
                          'feature_vector': [1,1,1], 
                          'text': u'testing paragraph for article 2',
                          'is_recipe': True}
        self.small_data = [(self.material_id_1, self.paragraph_data_1)]
        self.medium_data = [(self.material_id_1, self.paragraph_data_1), (self.material_id_1, self.paragraph_data_2)]

    def get_one(self):
        phelpers.add_paragraphs(self.connection, self.small_data)
        paragraphs = phelpers.get_paragraphs_of_query(self.connection, self.material_id_1, 5)

        self.assertTrue(paragraphs.count() == 1)
    
        phelpers.remove_paragraphs(self.connection, self.small_data)

    def get_many(self):
        phelpers.add_paragraphs(self.connection,self.medium_data)
        paragraphs = phelpers.get_paragraphs_of_query(self.connection, self.material_id_1, 5)
        self.assertTrue(paragraphs.count() == 2)

        phelpers.remove_paragraphs(self.connection, self.medium_data)

    def test_all(self):
        self.pa_collection.remove(self.paragraph_data_1)
        self.pa_collection.remove(self.paragraph_data_2)
        self.qy_collection.remove({'_id': self.material_id_1})

        self.get_one()
        self.get_many()

        self.pa_collection.remove(self.paragraph_data_1)
        self.pa_collection.remove(self.paragraph_data_2)
        self.qy_collection.remove({'_id': self.material_id_1})





