from json import loads
from synthesisapi.schemas import (target_entity)
from unittest import TestCase

class SchemaTester(TestCase):
  def setUp(self):
    pass
  def test_build(self):
    self.target_entity = target_entity

