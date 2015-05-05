# File containing functions dealing with feedback

'''
'''
def getAllFeedback(connection):
    fb_collection = connection['synthesis-api'].feedback
    cursor = fb_collection.Feedback.find()

    return list(cursor.limit(cursor.count()))

def getIsRecipeFeedback(connection):
    #   Gets all the feedback regarding if the paragraph is a recipe paragraph
    #   Output:
    #       {'ok': A, 'result': B}
    #       A       indicates if the function was successful
    #       B       a list of 
    fb_collection = connection['synthesis-api'].feedback
    return fb_collection.aggregate([
                {'$match': {'type': 'IS_RECIPE'}},
                {'$group': {'_id': '$paragraph_id', "feedback": { '$push': '$value'} }}])
'''
'''
def getIsRelatedRecipeFeedback(connection):
    fb_collection = connection['synthesis-api'].feedback
    return fb_collection.aggregate([
                {'$match': {'type': 'IS_RELATED_RECIPE', 'material_id' : {'$exists': True}}},
                {'$group': {'_id': {'paragraph_id': '$paragraph_id', 'material_id': '$material_id'}, 
                            "feedback": { '$push': '$value'} }}])
    
''' permanently removes feedback data from table
'''
def removeAllFeedback(connection):
    fb_collection = connection['synthesis-api'].feedback
    fb_collection.remove()

'''
'''
def createFeedback(connection, material_id, paragraph_id, user_id, ftype, value):
    fb_collection = connection['synthesis-api'].feedback
    feedback = fb_collection.Feedback()
    feedback['material_id'] = material_id.decode('unicode-escape') 
    feedback['paragraph_id'] = paragraph_id.decode('unicode-escape')
    feedback['user_id'] = user_id.decode('unicode-escape')
    feedback['type'] = ftype.decode('unicode-escape')
    feedback['value'] = value

    feedback.save()