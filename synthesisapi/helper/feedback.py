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