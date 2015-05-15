import pymongo
# File containing functions dealing with feedback

def getAllFeedback(connection):
    #   Returns a list of all the feedback in the database
    #   Input:      connection
    #   Output:     list of feedback objects in json format
    fb_collection = connection['synthesis-api'].feedback
    try:
        cursor = fb_collection.Feedback.find()
    except TypeError:
        return []

    return list(cursor.limit(cursor.count()))

def getIsRecipeFeedback(connection):
    #   Gets all the feedback regarding if the paragraph is a recipe paragraph
    #   Output:
    #       {'ok': A, 'result': B}
    #       A       indicates if the function was successful
    #       B       a list of {"_id": <paragraph_id>, "feedback": C}
    #               C is a list of feedback scores for that given paragraph_id
    fb_collection = connection['synthesis-api'].feedback
    return fb_collection.aggregate([
                {'$match': {'type': 'IS_RECIPE'}},
                {'$group': {'_id': '$paragraph_id', "feedback": { '$push': '$value'} }}])

def getIsRelatedRecipeFeedback(connection):
    #   Gets all the feedback regarding if the paragraph is a recipe for the material_id
    #   Output:
    #       {'ok': A, 'result': B}
    #       A       indicates if the function was successful
    #       B       a list of {"_id": {'paragraph_id': <paragraph_id>, 'material_id': <material_id>, "feedback": C}
    #               C is a list of feedback scores for that given paragraph_id /material_id pair
    fb_collection = connection['synthesis-api'].feedback
    return fb_collection.aggregate([
                {'$match': {'type': 'IS_RELATED_RECIPE', 'material_id' : {'$exists': True}}},
                {'$group': {'_id': {'paragraph_id': '$paragraph_id', 'material_id': '$material_id'}, 
                            "feedback": { '$push': '$value'} }}])

def removeAllFeedbackBefore(connection, time):
    #   Removes all the feedback created before a given time
    #   Input:
    #       time    the date in seconds
    #   Output:
    fb_collection = connection['synthesis-api'].feedback
    try:
        fb_collection.remove({'date_creation': {'$lt': time}})
        return True
    except pymongo.errors.OperationFailure: 
        return False

def removeAllRelatedFeedbackBefore(connection, time):
    #   Removes all the related feedback created before a given time
    #   Input:
    #       time    the date in seconds
    #   Output:
    fb_collection = connection['synthesis-api'].feedback
    try:
        fb_collection.remove({'type': 'IS_RELATED_RECIPE','date_creation': {'$lt': time}})
        return True
    except pymongo.errors.OperationFailure:
        return False

def removeAllIsRecipeFeedbackBefore(connection, time):
    #   Removes all the is recipe feedback created before a given time
    #   Input:
    #       time    the date in seconds
    #   Output:
    fb_collection = connection['synthesis-api'].feedback
    try:
        fb_collection.remove({'type': 'IS_RECIPE','date_creation': {'$lt': time}})
        return True
    except pymongo.errors.OperationFailure:
        return False

def createFeedback(connection, material_id, paragraph_id, user_id, ftype, value):
    #   Creates a feedback object given parameters
    #   Input:
    #       
    #   Output:
    #       success         Boolean indicating success
    fb_collection = connection['synthesis-api'].feedback
    feedback = fb_collection.Feedback()
    feedback['material_id'] = material_id.decode('unicode-escape') 
    feedback['paragraph_id'] = paragraph_id.decode('unicode-escape')
    feedback['user_id'] = user_id.decode('unicode-escape')
    feedback['type'] = ftype.decode('unicode-escape')
    feedback['value'] = value
    try:
        feedback.save()
        return True
    except pymongo.errors.OperationFailure:
        return False
