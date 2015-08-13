target_entity = {
  'item_title': 'material',
  'schema': {
    'paragraphs': {
      'type': 'list'
    },
    'mpid': {
      'type': 'string',
      'required': True,
      'unique': True
    }
  },
  'additional_lookup': {
    'url': 'regex("[\w]+")',
    'field': 'mpid'
  }
}