# File containing functions dealing with feedback

'''
'''
def getAllFeedback(connection):
    fb_collection = connection['synthesis-api'].feedback
    return fb_collection.Feedback.find().toArray()

''' permanently removes feedback data from table
'''
def removeAllFeedback(connection):
    fb_collection = connection['synthesis-api'].feedback
    fb_collection.remove()

def createFeedback(connection, material_id, paragraph_id, user_id, ftype, value):
    fb_collection = connection['synthesis-api'].feedback
    feedback = fb_collection.Feedback()
    feedback['material_id'] = u'' 
    feedback['paragraph_id'] = u''
    feedback['user_id'] = u''
    feedback['type'] # IS_RECIPE or IS_RELATED_RECIPE (unicode)
    feedback['value'] #answer to the question
    feedback.save()