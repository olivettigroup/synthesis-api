from json import loads
from mongokit import Connection
from synthesisapi.models import (Paragraph, Query, Feedback)
import synthesisapi.helper.paragraph as phelpers
import synthesisapi.helper.feedback as fhelpers
from unittest import TestCase

class ModelTester(TestCase):
  def setUp(self):
    print "hi"

  def test_build(self):
    self.assertTrue(True)

