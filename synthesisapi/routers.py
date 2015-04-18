from mongokit import Connection, Document
from flask import Flask
from models import Paragraph

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
# 

# =================== MIT SERVER - SYNTHESIS-API

# update_paragraphs()
    # input: {add: {material_id: [paragraphs]}, subtract: {material_id: [paragraphs]}
    # input: (TODO) list_of_papers_covered
    # loops through received paragraphs and updates paragraphs and queries

# send_feedback_to(server)
    # Sends all feedback that hasn't been sent to given server

 
# =================== 3RD PARTIES - SYNTHESIS-API

# get_paragraphs(material_id)

# get_paragraphs_formatted(material_id)
    # perhaps formatted?

# record_feedback(material_id, paragraph_id, feedback)
    # sanitize inputs!
    # TODO: do we want to store feedback as 1/-1 for now, or complex object 
    # accpts true or false: to the question is_recipe?
    # user_id
    # paragraph_id
    # material_id

@app.route("/update_paragraphs", methods=['PUT'])
def update_paragraphs():
    # input: type: 1 = addition, -1 subtraction
    # input: material_id, paragraph
    # request.form["var"]
    return "Hello World!"


@app.route("/pull_feedback_data", methods=['GET'])
def pull_feedback_data():
    # might want to only allow certain users to do this? or not even
    # make this a method
    # When feedback is pulled, give userid and timestamp as well
    return "pull feedback data"

@app.route("/get_paragraphs/<material_id>", methods=['GET'])
def get_paragraphs(material_id):
    # request.args.get('key','')
    return material_id

@app.route("/get_paragraphs_formatted/<material_id>", methods=['GET'])
def get_paragraphs_formatted(material_id):
    return "get paragraphs formatted: " +  material_id

@app.route("/record_feedback", methods=['POST'])
def record_mpid_feedback():
    return "record feedback"

def record_is_recipe_feedback():
    return "is recipe feedback"

if __name__ == "__main__":
    app.run()
