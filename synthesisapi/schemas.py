material = {
  'item_title': 'material',
  'schema': {
    'dois': {
      'type': 'list'
    },
    'associated_materials': {
      'type': 'list'
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
