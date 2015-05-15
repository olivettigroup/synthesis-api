from flask import jsonify
from mongokit import Connection, Document
from flask import Flask
from models import Paragraph, Query, Feedback
from flask import render_template
from flask import request
import helper.paragraph as pa_helper
import helper.feedback as fb_helper


# Database configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

# Flask Application configuration
app = Flask(__name__)
app.config.from_object(__name__)

# Connect to Database
connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])

connection.register([Paragraph])
connection.register([Query])
connection.register([Feedback])

# ================== TESTING

@app.route("/test")
def test():
    return render_template('test.html', name='vicky')

# =================== MIT SERVER - SYNTHESIS-API
# DONE
@app.route("/update_paragraphs", methods=['POST', 'PUT'])
def update_paragraphs():
    # Updates the list of paragraphs and queries
    # Input 
    #       update_type (int)      1 = addition, -1 subtraction TODO: might want to separate this into 2 functions
    #       material_id            
    #       paragraph_text  
    #       rank
    #       feature_vector         Each element in array concatenated by "," e.g. "1,2,3" = [1,2,3]
    #       is_recipe
    #       doi     
    # Output
    #       (success, error)
    #       where success is a boolean, and error is an error message
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
    # Pulls two types of considolated feedback data:
    #       1) Feedback on if a paragraph is a recipe
    #       2) Feedback on if a paragraph is a recipe for a specific material
    # Required: API Access @TODO
    #   
    # Output:
    #       {'related': is_related_recipe_feedback, 'is_recipe': is_recipe_feedback}
    #       Both of these are 

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
    #   Function used by users to confirm they hae pulled data until time
    #   Input:
    #       time            the date + time they pulled the data (in secs)
    #
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
    # Retrieves a list of paragraphs indicating steps for given material_id
    # Input 
    #       material_id (int)      (TODO) type of material_id
    #       format (string)         Format the data will be in.
    #       
    # Output
    #       paragraphs (array)      Array of paragraph objects
    #                               (TODO) get rid of _id
    #       
    amt = 5
    result = pa_helper.get_paragraphs_of_query(connection, material_id, amt)
    return jsonify(paragraphs=result)

@app.route("/get_paragraphs_formatted/<material_id>", methods=['GET'])
def get_paragraphs_formatted(material_id, format="json"):
    if (format == 'json'):
        return get_paragraphs(material_id)
    else:
        return get_paragraphs(material_id)

@app.route("/record_feedback", methods=['POST'])
def record_mpid_feedback():
    # TODO probably want some authorization of 3rd party API?
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

    # TODO: add cooldown time so cant record from same user
    return jsonify(success=result, error="")

@app.route("/record_is_recipe_feedback", methods=['POST'])
def record_is_recipe_feedback():
    # TODO probably want some authorization of 3rd party API?
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
    app.run()
