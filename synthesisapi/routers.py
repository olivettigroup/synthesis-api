from mongokit import Connection, Document
from flask import Flask
from models import Paragraph, Query, Feedback
from flask import render_template
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

@app.route("/update_paragraphs", methods=['PUT'])
def update_paragraphs():
    # Updates the list of paragraphs and queries
    # Input 
    #       update_type (int)      1 = addition, -1 subtraction
    #       data (array)           [(material_id, paragraph)...]
    #                              paragraph = {...}
    # Output
    #       (success, error)
    #       where success is a boolean, and error is an error message
    update_type = request.form["update_type"]
    if not update_type in (-1,1):
        return (False, {message: "Update Type is not a valid integer (-1,1)", success: False})

    if update_type == 1:
        pa_helper.add_paragraphs(connection, request.form["data"])

    else:
        pa_helper.remove_paragraphs(connection, request.form["data"])

    return (True, None)


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
    
    is_recipe_feedback = fb_helper.getIsRecipeFeedback(connection)
    is_related_recipe_feedback = fb_helper.getIsRelatedRecipeFeedback(connection)    

    fb_helper.removeAllFeedback(connection)  #could potentially move this to after feedback is sent

    return {'related': is_related_recipe_feedback, 'is_recipe': is_recipe_feedback}

 
# =================== 3RD PARTIES - SYNTHESIS-API

@app.route("/get_paragraphs/<material_id>", methods=['GET'])
def get_paragraphs(material_id):
    # Retrieves a list of paragraphs indicating steps for given material_id
    # Input 
    #       material_id (int)      (TODO) type of material_id
    #       
    # Output
    #       paragraphs (array)      Array of paragraph objects
    #                               (TODO) get rid of _id
    #       
    # TODO: defaulting to returning 5??
    amt = 5
    return list(get_paragraphs_of_query(connection, material_id, amt).limit(amt))

@app.route("/get_paragraphs_formatted/<material_id>", methods=['GET'])
def get_paragraphs_formatted(material_id, format="plain/text"):
    switch(format){
        case "plain/text":
            return get_paragraphs
    }

    return "get paragraphs formatted: " +  material_id

@app.route("/record_feedback", methods=['POST'])
def record_mpid_feedback():
    # TODO probably want some authorization of 3rd party API?
    user_id = request.form["user_id"]
    paragraph_id = request.form["paragraph_id"]
    material_id = request.form["material_id"]  
    isvalid = pa_helper.validate_paragraph_query(connection, paragraph_id, material_id)
    if not isvalid:
        return {'error': True, 'msg': "Not valid material_id / paragraph_id pair"}
    value = request.form["value"]
    if value not in [-1, 1]:
        return {'error': True, 'msg': "Not valid value"}
    ftype = "IS_RELATED_RECIPE"

    fb_helper.createFeedback(connection, material_id, paragraph_id, user_id, ftype, value)

    # TODO: add cooldown time so cant record from same user
    return "is correct pair feedback"

@app.route("/record_is_recipe_feedback", methods=['POST'])
def record_is_recipe_feedback():
    ftpye = "IS_RECIPE"
    # TODO probably want some authorization of 3rd party API?
    user_id = request.form["user_id"]
    paragraph_id = request.form["paragraph_id"]
    material_id = request.form["material_id"]   #TODO: might not want to require this later
    isvalid = pa_helper.validate_paragraph_query(connection, paragraph_id, material_id)
    if not isvalid:
        return {'error': True, 'msg': "Not valid material_id / paragraph_id pair"}
    value = request.form["value"]
    if value not in [-1, 1]:
        return {'error': True, 'msg': "Not valid value"}
    ftype = "IS_RELATED_RECIPE"

    fb_helper.createFeedback(connection, material_id, paragraph_id, user_id, ftype, value)
    return "is recipe feedback"

if __name__ == "__main__":
    app.run()
