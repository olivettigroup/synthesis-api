# File containing helper functions dealing
# With paragraph and query objects

''' Adds paragraphs to given queries
    Input:
        connection      mongodb connection
                        required: have registered Paragraph, Query
    
        data            [(material_id, paragraph)...]                             
                        paragraph = {...}
    Output:
'''
def add_paragraphs(connection,data):
    pa_collection = connection['synthesis-api'].paragraphs
    qy_collection = connection['synthesis-api'].queries

    # TODO: do we need a try/catch?
    for (material_id, paragraph) in data:
        # Creating a paragraph object if it does not exist
        paragraph_object = pa_collection.Paragraph.find_one_and_update(
            {'doi': paragraph.doi, 'text': paragraph.text},
            { '$setOnInsert': { 'feature_vector': paragraph.feature_vector,
                             'is_recipe': paragraph.is_recipe }
            },
            upsert=True)
         
        # Incudes paragraph into query
        query = qy_collection.Query.find_one_and_update(
            {_id: material_id},
            {   '$addToSet': {'paragraphs': paragraph_object._id },
                '$setOnInsert': {
                    'paragraphs': [paragraph_object._id]
                }
            },
            upsert=True)


''' Removes paragraphs for the given queries
    Input:
        connection      mongodb connection
                        required: have registered Paragraph, Query
    
        data            [(material_id, paragraph)...]                             
                        paragraph = {...}
    Output:
'''
def remove_paragraphs(connection,data):
    pa_collection = connection['synthesis-api'].paragraphs
    qy_collection = connection['synthesis-api'].queries

    # TODO: do we need a try/catch?
    for (material_id, paragraph) in data:
        # Finds the paragraph object
        paragraph_object = pa_collection.Paragraph.find_one(
            {'doi': paragraph.doi, 'text': paragraph.text})
         
        # Removes paragraph object from query  
        query = qy_collection.Query.find_one_and_update(
            {_id: material_id},
            { '$pull': { 'paragraphs': paragraph_object._id }})
