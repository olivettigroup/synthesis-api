from json import loads
from synthesisapi.schemas import (material)
from unittest import TestCase

class SchemaTester(TestCase):
  def setUp(self):
    pass
    
  def test_build(self):
    self.material = material
