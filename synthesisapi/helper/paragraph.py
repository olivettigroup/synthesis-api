# File containing helper functions dealing
# With paragraph and query objects
from bson import ObjectId

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
        paragraph_object = pa_collection.Paragraph.find_and_modify(
            {'doi': paragraph['doi'], 'text': paragraph['text']},
            update={'$setOnInsert': { 
                            'feature_vector': paragraph['feature_vector'],
                            'is_recipe': paragraph['is_recipe'],
                            'doi': paragraph['doi'], 
                            'text': paragraph['text'] }
            },
            upsert=True,
            new=True)

        print paragraph_object
         
        # Incudes paragraph into query
        query = qy_collection.Query.find_and_modify(
            {'_id': material_id},
            update=
            {   '$addToSet': {'paragraphs': paragraph_object['_id'] },
                '$set': {'_id': material_id}
            },
            upsert=True,
            new=True)


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
            {'doi': paragraph['doi'], 'text': paragraph['text']})
        
        if paragraph_object is not None:
            # Removes paragraph object from query  
            query = qy_collection.Query.find_and_modify(
                {'_id': material_id},
                update={ '$pull': { 'paragraphs': paragraph_object['_id'] }})
