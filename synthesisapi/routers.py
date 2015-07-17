from flask import jsonify
from mongokit import Connection, Document
from flask import Flask
from models import Paragraph, Query, Feedback
from flask import render_template
from flask import request
from os import environ 
import helper.paragraph as pa_helper
import helper.feedback as fb_helper


# Database configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_URI = environ.get('MONGOLAB_URI')

# Flask Application configuration
app = Flask(__name__)
app.config.from_object(__name__)


# ================== TESTING

@app.route('/')
def main():
  '''
  Default main route - doesn't actually do anything.
  '''
  return 'Welcome to the Synthesis API! (Use POST to actually do things)'

@app.route("/test")
def test():
  '''
  Renders view for the API testing form 

  .. todo:: Disable in production mode
  '''
  return render_template('test.html', name='vicky')


# =================== MIT SERVER <-> SYNTHESIS-API

@app.route("/update_paragraphs", methods=['POST', 'PUT'])
def update_paragraphs():
  '''
  Updates the list of paragraphs and queries (POST/PUT ROUTE)
  
  (Params are all REST params)

  :param update_type: 1 = addition, -1 subtraction
  :type update_type: int
  :param material_id: Relevant material ID
  :type material_id: unicode 
  :param paragraph_text: raw text of the paragraph 
  :type paragraph_text: unicode 
  :param rank: Relevance ranking for this paragraph (i.e. relevance to target material)
  :type rank: int 
  :param feature_vector:  Each element in array concatenated by "," e.g. "1,2,3" = [1,2,3]
  :type feature_vector: unicode 
  :param is_recipe: 0 = not a recipe paragraph, 1 = is a recipe paragraph 
  :type is_recipe: int 
  :param doi: DOI of the paper the paragraph belongs to 
  :type doi: unicode 

  :returns: Success or error (returns error message on error)
  :rtype: json 

  .. todo:: Internal API Key required 
  '''

  try:
    update_type = int(request.form["update_type"])
  except ValueError:
    return jsonify(success=False, error_message="Update Type is not a valid integer (-1,1)")

  if not update_type in (-1,1):
    return jsonify(success=False, error_message="Update Type is not a valid integer (-1,1)")

  paragraph = {
    'doi': request.form["doi"],
    'text': request.form["paragraph_text"],
    'is_recipe': request.form["is_recipe"],
    'feature_vector': pa_helper.parse_feature_vector(request.form["feature_vector"])
  } 

  if update_type == 1:
    result = pa_helper.add_paragraphs(connection, request.form["material_id"], paragraph, request.form["rank"])
  else:
    result = pa_helper.remove_paragraphs(connection, request.form["material_id"], paragraph, request.form["rank"])

  if not result:
    return jsonify(success=False, error="Could not add/remove paragraphs")

  return jsonify(success=True, error=None)


@app.route("/pull_feedback_data", methods=['GET'])
def pull_feedback_data():
  '''
  Pulls two types of consolidated feedback data for all paragraphs: (GET ROUTE)
  
  1. Feedback on if a paragraph is a recipe
  2. Feedback on if a paragraph is a recipe for a specific material

    
  :returns: JSON with consolidated feedback 

  ::

    {
      'related': is_related_recipe_feedback, 
      'is_recipe': is_recipe_feedback
    }

  :rtype: json 

  .. todo:: Required: Internal API Key Access
  '''
 
  # Getting is recipe feedback
  is_recipe_feedback = 'No data'
  recipeContent = fb_helper.getIsRecipeFeedback(connection)
  if (recipeContent['ok'] == 1):
    is_recipe_feedback = recipeContent
  else:
    is_recipe_feedback = 'Error: Could not retrieve.'
  
  # Getting is related recipe feedback
  isRelatedContent = fb_helper.getIsRelatedRecipeFeedback(connection)    
  if (isRelatedContent['ok'] == 1):
    is_related_recipe_feedback = isRelatedContent
  else:
    is_related_recipe_feedback = 'Error: Could not retrieve.'

  return jsonify(related=is_related_recipe_feedback, is_recipe=is_recipe_feedback)

@app.route("/confirm_feedback_data_pulled", methods=['PUT'])
def indicate_successful_pull():
  '''
  Function used by internal users to confirm they have pulled data (PUT ROUTE)

  Wipes out all feedback older than the pull request which was succesfully pulled 

  (Params are all REST params)

  :param time: the date + time they pulled the data (in unicode timestamp secs)
  :type time: int 
  :param got_related: If you successfully got is_related_recipe
  :type got_related: bool  
  :param got_is_recipe: If you successfully got is_recipe
  :type got_is_recipe: bool

  :returns: Whether or not error was successful 
  :rtype: json 
  '''
  
  time = request.form["time"]
  got_related = request.form["got_related"]
  got_is_recipe = request.form["got_is_recipe"]

  if (got_related and got_is_recipe):
    result = fb_helper.removeAllFeedbackBefore(connection, time)
  elif (got_related):
    result = fb_helper.removeAllRelatedFeedbackBefore(connection, time)
  else:
    result = fb_helper.removeAllIsRecipeFeedbackBefore(connection, time)

  return jsonify(success=result, error='')
 

# =================== 3RD PARTIES - SYNTHESIS-API

@app.route("/get_paragraphs/<material_id>", methods=['GET'])
def get_paragraphs(material_id):
  '''
  Retrieves a list of paragraphs indicating steps for given material_id (GET ROUTE)

  (Params are all REST params)

  :param material_id: (TODO) type of material_id
  :type material_id: str 

  :returns:  Array of paragraph objects
  :rtype: json    
  '''

  amt = 5
  result = pa_helper.get_paragraphs_of_query(connection, material_id, amt)
  return jsonify(paragraphs=result)

@app.route("/get_paragraphs_formatted/<material_id>", methods=['GET'])
def get_paragraphs_formatted(material_id, format="json"):
  '''
  Wrapper for get_paragraphs, with a format specified.

  (Params are all REST params)

  :param material_id: type of material_id
  :type material_id: str 
  :param format: Format the data will be in
  :type format: unicode

  :returns: Array of formatted paragraph objects
  :rtype: json   

  .. todo:: Implement material id 
  .. todo:: Implement LaTeX 
  '''

  if (format == 'json'):
    return get_paragraphs(material_id)
  else:
    return get_paragraphs(material_id)

@app.route("/record_is_related_feedback", methods=['POST'])
def record_is_related_feedback():
  '''
  Records feedback for if a paragraph is related to the correct material 

  (Params are all REST params)

  :param user_id: ID of user submitting the feedback 
  :type user_id: unicode
  :param paragraph_id: ID of paragraph 
  :type paragraph_id: unicode 
  :param material_id: ID of relevant material 
  :type material_id: unicode 

  :returns: Success or failure of request 
  :rtype: json

  .. todo :: Add cooldown time so can't record from same user
  .. todo :: 3rd party API key validation 
  '''

  ftype = "IS_RELATED_RECIPE"
  user_id = request.form["user_id"]
  paragraph_id = request.form["paragraph_id"]
  material_id = request.form["material_id"]    

  #Input Checking
  try:
    value = int(request.form["value"])
  except ValueError:
    return jsonify(success=False, error='Not valid value (-1 or 1)')
  if value not in (-1, 1):
    return jsonify(success=False, error="Not valid value (-1 or 1)")
  if not pa_helper.validate_paragraph_query(connection, paragraph_id, material_id):
    return jsonify(success=False, error="Not valid material_id / paragraph_id pair")
  
  # Creating Feedback
  result = fb_helper.createFeedback(connection, material_id, paragraph_id, user_id, ftype, value)
 
  return jsonify(success=result, error="")

@app.route("/record_is_recipe_feedback", methods=['POST'])
def record_is_recipe_feedback():
  '''
  Records feedback for if a paragraph is related to the correct material 

  (Params are all REST params)

  :param user_id: ID of user submitting the feedback 
  :type user_id: unicode
  :param paragraph_id: ID of paragraph 
  :type paragraph_id: unicode 
  :param material_id: ID of relevant material 
  :type material_id: unicode  

  :returns: Success or failure of request 
  :rtype: json

  .. todo :: Add cooldown time so can't record from same user
  .. todo :: 3rd party API key validation
  '''

  ftpye = "IS_RECIPE"
  user_id = request.form["user_id"]
  paragraph_id = request.form["paragraph_id"]
  material_id = request.form["material_id"]   #TODO: might not want to require this later
  isvalid = pa_helper.validate_paragraph_query(connection, paragraph_id, material_id)
  
  # Input Checking
  try:
    value = request.form["value"]  
  except ValueError:
    return jsonify(success=False, error='Not valid value (-1 or 1)') 
  if value not in (-1, 1):
    return jsonify(success=False, error="Not valid value (-1 or 1)")
  if not isvalid:
    return jsonify(success=False, error="Not valid material_id / paragraph_id pair")

  result = fb_helper.createFeedback(connection, material_id, paragraph_id, user_id, ftype, value)
  
  return jsonify(success=result, error="")

if __name__ == "__main__":
  # Connect to Database
  connection = Connection(MONGODB_URI)
  connection.register([Paragraph, Query, Feedback])

  app.run()
