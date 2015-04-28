from mongokit import Connection, Document
from flask import Flask
from models import Paragraph, Query, Feedback
from flask import render_template
import helper.paragraph 


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
        add_paragraphs(connection, request.form["data"])

    else:
        remove_paragraphs(connection, request.form["data"])

    return (True, None)


@app.route("/pull_feedback_data", methods=['GET'])
def pull_feedback_data():
    # TODO: only allow certain api accesss
    # TODO: make remove occur later??
    feedback_data = getAllFeedback(connection)
    removeAllFeedback(connection)

    return feedback_data

 
# =================== 3RD PARTIES - SYNTHESIS-API

# record_feedback(material_id, paragraph_id, feedback)
    # sanitize inputs!
    # TODO: do we want to store feedback as 1/-1 for now, or complex object 
    # accpts true or false: to the question is_recipe?
    # user_id
    # paragraph_id
    # material_id

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
    return get_paragraphs_of_query(connection, material_id, 5).toArray()

@app.route("/get_paragraphs_formatted/<material_id>", methods=['GET'])
def get_paragraphs_formatted(material_id):
    # TODO what kind of formatting?
    return "get paragraphs formatted: " +  material_id

@app.route("/record_feedback", methods=['POST'])
def record_mpid_feedback():
    # TODO probably want some authorization of 3rd party API?
    # TODO how do we ensure that user_id is a real user id - security
    # TODO, are we compiling here?
    # TODO: check valid material id here?
    request.form["user_id"]
    request.form["paragraph_id"]
    request.form["material_id"]
    request.form[""]
    return "record feedback"

def record_is_recipe_feedback():
    # TODO
    # TODO probably want some authorization of 3rd party API?
    # TODO how do we ensure that user_id is a real user id - security
    return "is recipe feedback"

if __name__ == "__main__":
    app.run()
