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
        self.small_data = [(self.material_id_1, self.paragraph_data_1, 0)]
        self.medium_data = [(self.material_id_1, self.paragraph_data_1, 0), (self.material_id_2, self.paragraph_data_2, 0)]
        self.large_data = [(self.material_id_1, self.paragraph_data_1, 0), 
                           (self.material_id_2, self.paragraph_data_2, 0),
                           (self.material_id_1, self.paragraph_data_3, 0)]


    def single(self):
        # Adding a paragraph
        phelpers.add_paragraphs(self.connection, self.small_data)

        # Checking that the paragraph object was created
        paragraph_object = self.pa_collection.Paragraph.find_one(self.paragraph_data_1) 
        
        self.assertTrue(self.pa_collection.count() == 1)
        self.assertTrue(paragraph_object is not None)

        # Checking that the query object was created
        self.assertTrue(self.qy_collection.count() == 1)
        
        query_object = self.qy_collection.Query.find_one({'material_id': self.material_id_1, 'paragraph': paragraph_object['_id']})
        self.assertTrue(query_object is not None)

        # Removing the paragraph
        phelpers.remove_paragraphs(self.connection, self.small_data)

        # Checking that the query object was removed
        qy_object = self.qy_collection.Query.find_one({'material_id': self.material_id_1, 'paragraph': paragraph_object['_id']})
        
        self.assertTrue(qy_object is None )
        self.assertTrue(self.qy_collection.count() == 0)

        # Removing the paragraph
        self.pa_collection.remove(self.paragraph_data_1)
        self.assertTrue(self.pa_collection.count() == 0)

    def multiple(self):
        phelpers.add_paragraphs(self.connection, self.medium_data)

        # Checking that the paragraph objects was created
        paragraph_object_1 = self.pa_collection.Paragraph.find_one(self.paragraph_data_1) 
        paragraph_object_2 = self.pa_collection.Paragraph.find_one(self.paragraph_data_2) 
        self.assertTrue(self.pa_collection.count() == 2)
        self.assertTrue(paragraph_object_1 is not None)
        self.assertTrue(paragraph_object_2 is not None)

        # Checking that the query objects was created
        query_object_1 = self.qy_collection.Query.find_one({'material_id': self.material_id_1, 'paragraph': paragraph_object_1['_id']})
        query_object_2 = self.qy_collection.Query.find_one({'material_id': self.material_id_2, 'paragraph': paragraph_object_2['_id']})
        self.assertTrue(self.qy_collection.count() == 2)
        self.assertTrue(query_object_1 is not None)
        self.assertTrue(query_object_2 is not None)
        
        # Removing the paragraph
        phelpers.remove_paragraphs(self.connection, self.medium_data)

        # Checking that the query objects do not exist
        qy_object_1 = self.qy_collection.Query.find_one({'material_id': self.material_id_1, 'paragraph': paragraph_object_1['_id']})
        qy_object_2 = self.qy_collection.Query.find_one({'material_id': self.material_id_2, 'paragraph': paragraph_object_2['_id']})
        self.assertTrue(qy_object_1 is None )
        self.assertTrue(qy_object_2 is None )
        self.assertTrue(self.qy_collection.count() == 0)

        # Removing the paragraph
        self.pa_collection.remove(self.paragraph_data_1)
        self.pa_collection.remove(self.paragraph_data_2)
        self.assertTrue(self.pa_collection.count() == 0)

    def interleaved_multiple(self):
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
        query_object_1 = self.qy_collection.Query.find_one({'material_id': self.material_id_1, 'paragraph': paragraph_object_1['_id']})
        query_object_2 = self.qy_collection.Query.find_one({'material_id': self.material_id_2, 'paragraph': paragraph_object_2['_id']})
        query_object_3 = self.qy_collection.Query.find_one({'material_id': self.material_id_1, 'paragraph': paragraph_object_3['_id']})
        self.assertTrue(self.qy_collection.count() == 3)
        self.assertTrue(query_object_1 is not None)
        self.assertTrue(query_object_2 is not None)
        
        # Removing one paragraph
        phelpers.remove_paragraphs(self.connection, self.small_data)

        # Checking that the query object has one less
        self.assertTrue(self.qy_collection.count() == 2)
        
        # Removing all paragraphs
        phelpers.remove_paragraphs(self.connection, self.large_data)

        # Checking that all the query objects were removed
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
        self.qy_collection.remove({'material_id': self.material_id_1})
        self.qy_collection.remove({'material_id': self.material_id_2})

        self.single()
        self.multiple()
        self.interleaved_multiple()

        self.pa_collection.remove(self.paragraph_data_1)
        self.pa_collection.remove(self.paragraph_data_2)
        self.pa_collection.remove(self.paragraph_data_3)
        self.qy_collection.remove({'material_id': self.material_id_1})
        self.qy_collection.remove({'material_id': self.material_id_2})


class ParagraphGetTester(TestCase):
    def setUp(self):
        self.connection = Connection()
        self.connection.register([Paragraph])
        self.connection.register([Query])

        self.pa_collection = self.connection['synthesis-api'].paragraphs
        self.qy_collection = self.connection['synthesis-api'].queries

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
        self.small_data = [(self.material_id_1, self.paragraph_data_1, 0)]
        self.medium_data = [(self.material_id_1, self.paragraph_data_1, 0), (self.material_id_1, self.paragraph_data_2, 0)]
        self.mix_data = [(self.material_id_1, self.paragraph_data_1, 0), 
                         (self.material_id_1, self.paragraph_data_2, 0),
                         (self.material_id_2, self.paragraph_data_3, 0)]


    def get_one(self):
        phelpers.add_paragraphs(self.connection, self.small_data)
        paragraphs = phelpers.get_paragraphs_of_query(self.connection, self.material_id_1, 5)

        self.assertTrue(paragraphs.count() == 1)
        self.assertTrue(list(paragraphs.limit(1))[0]['doi'] == 1)
    
        phelpers.remove_paragraphs(self.connection, self.small_data)

    def get_many(self):
        phelpers.add_paragraphs(self.connection,self.medium_data)
        paragraphs = phelpers.get_paragraphs_of_query(self.connection, self.material_id_1, 5)
        self.assertTrue(paragraphs.count() == 2)

        phelpers.remove_paragraphs(self.connection, self.medium_data)

    def get_mix(self):
        phelpers.add_paragraphs(self.connection, self.mix_data)
        paragraphs = phelpers.get_paragraphs_of_query(self.connection, self.material_id_1, 5)
        self.assertTrue(paragraphs.count() == 2)

        paragraphs = phelpers.get_paragraphs_of_query(self.connection, self.material_id_2, 5)
        self.assertTrue(paragraphs.count() == 1)

        phelpers.remove_paragraphs(self.connection, self.mix_data)


    def test_all(self):
        self.pa_collection.remove(self.paragraph_data_1)
        self.pa_collection.remove(self.paragraph_data_2)
        self.pa_collection.remove(self.paragraph_data_3)
        self.qy_collection.remove({'material_id': self.material_id_1})
        self.qy_collection.remove({'material_id': self.material_id_2})

        self.get_one()
        self.get_many()
        self.get_mix()

        self.pa_collection.remove(self.paragraph_data_1)
        self.pa_collection.remove(self.paragraph_data_2)
        self.pa_collection.remove(self.paragraph_data_3)
        self.qy_collection.remove({'material_id': self.material_id_1})
        self.qy_collection.remove({'material_id': self.material_id_2})

class FeedbackCreateTester(TestCase):
    def setUp(self):
        # MongoDB Setup
        self.connection = Connection()
        self.connection.register([Feedback])

        self.fb_collection = self.connection['synthesis-api'].feedback

        # Data setup
        self.material_id_1 = '9999999'
        self.material_id_2 = '1000000'
        self.f1 = {'material_id': self.material_id_1, 
                   'paragraph_id': '1', 
                   'user_id': u'vickyg',
                   'type': "IS_RELATED_RECIPE",
                   'value': True}
        self.f2 = {'material_id': self.material_id_2, 
                   'paragraph_id': '2', 
                   'user_id': u'vickyg1',
                   'type': "IS_RECIPE",
                   'value': True}
        self.f3 = {'material_id': self.material_id_1, 
                   'paragraph_id': '1', 
                   'user_id': u'vickyg1',
                   'type': "IS_RELATED_RECIPE",
                   'value': False}

    def is_recipe_create_test(self):
        fhelpers.createFeedback(self.connection,
                                self.f1['material_id'],
                                self.f1['paragraph_id'],
                                self.f1['user_id'],
                                self.f1['type'],
                                self.f1['value'] )

        fb_object = self.fb_collection.Feedback.find_one(self.f1)
        self.assertTrue(fb_object is not None)

        # Delete feedback
        self.fb_collection.remove(self.f1)

    def is_related_recipe_create(self):
        fhelpers.createFeedback(self.connection,
                                self.f2['material_id'],
                                self.f2['paragraph_id'],
                                self.f2['user_id'],
                                self.f2['type'],
                                self.f2['value'] )

        fb_object = self.fb_collection.Feedback.find_one(self.f2)
        self.assertTrue(fb_object is not None)

        # Delete feedback
        self.fb_collection.remove(self.f2)


    def test_suite(self):
        self.fb_collection.remove(self.f1)
        self.fb_collection.remove(self.f2)

        self.is_related_recipe_create()
        self.is_recipe_create_test()

        self.fb_collection.remove(self.f1)
        self.fb_collection.remove(self.f2)

class FeedbackGetTester(TestCase):
    def setUp(self):
        # MongoDB Setup
        self.connection = Connection()
        self.connection.register([Feedback])

        self.fb_collection = self.connection['synthesis-api'].feedback

        # Data setup
        self.material_id_1 = '9999999'
        self.material_id_2 = '1000000'
        self.f1 = {'material_id': self.material_id_1, 
                   'paragraph_id': '1', 
                   'user_id': u'vickyg',
                   'type': "IS_RELATED_RECIPE",
                   'value': 1}
        self.f2 = {'material_id': self.material_id_2, 
                   'paragraph_id': '2', 
                   'user_id': u'vickyg1',
                   'type': "IS_RECIPE",
                   'value': 1}
        self.f3 = {'material_id': self.material_id_1, 
                   'paragraph_id': '1', 
                   'user_id': u'vickyg1',
                   'type': "IS_RELATED_RECIPE",
                   'value': -1}
        self.f4 = {'material_id': self.material_id_2, 
                   'paragraph_id': '1', 
                   'user_id': u'vickyg1',
                   'type': "IS_RELATED_RECIPE",
                   'value': -1}


    def check_get(self):
        for fb in [self.f1, self.f2, self.f3, self.f4]:
            fhelpers.createFeedback(self.connection,
                                    fb['material_id'],
                                    fb['paragraph_id'],
                                    fb['user_id'],
                                    fb['type'],
                                    fb['value'] )

        result = fhelpers.getIsRecipeFeedback(self.connection)
        items = result['result']
        self.assertTrue(result['ok'] == 1)
        self.assertTrue(len(items) == 1)
        self.assertTrue(items[0]['feedback'] == [1])

        result = fhelpers.getIsRelatedRecipeFeedback(self.connection)
        items = result['result']
        self.assertTrue(result['ok'] == 1)
        self.assertTrue(len(items) == 2)

        # Checking mateiral_id: 1 and paragraph: 1 were aggregated properly
        self.assertTrue(items[0]['feedback'] == [-1])
        self.assertTrue(items[1]['feedback'] == [1,-1])
        

    def test_suite(self):
        self.fb_collection.remove(self.f1)
        self.fb_collection.remove(self.f2)
        self.fb_collection.remove(self.f3)
        self.fb_collection.remove(self.f4)

        self.check_get()

        self.fb_collection.remove(self.f1)
        self.fb_collection.remove(self.f2)
        self.fb_collection.remove(self.f3)
        self.fb_collection.remove(self.f4)

