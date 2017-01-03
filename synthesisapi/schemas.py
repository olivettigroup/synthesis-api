material = {
  'item_title': 'material',
  'schema': {
    'sample_dois': {
      'type': 'list'
    },

    'associated_materials': {
      'type': 'list'
    },
    'temperature_histogram': {
      'type': 'dict',
      'schema': {
        'x': {'type': 'list'},
        'y': {'type': 'list'}
      }
    },
    'synthesis_descriptions': {
      'type': 'list'
    }
  }
}
