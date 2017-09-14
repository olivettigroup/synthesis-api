material = {
  'item_title': 'material',
  'additional_lookup': {
         'url': 'regex("[\w]+")',
         'field': 'name',
     },
  'schema': {
    'name': {
      'type': 'string',
      'unique': True,
      'required': True
    },
    'dois': {
      'type': 'list'
    },
    'associated_materials': {
      'type': 'list'
    },
    'associated_operations': {
      'type': 'list'
    },
    'topics': {
      'type': 'dict',
    },
    'temperature_histogram': {
      'type': 'dict',
      'schema': {
        'temperatures': {'type': 'list'},
        'frequencies': {'type': 'list'}
      }
    },
    'synthesis_descriptions': {
      'type': 'list'
    }
  }
}
