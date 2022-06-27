"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

member_db = FamilyStructure(last_name="Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET']) #all family members
def all_members():
    members = member_db.get_all_members()
    response_body = {
        "member": members
    }
    return jsonify(response_body), 200

@app.route("/members/<int:id>", methods=['GET']) # single family member
def get_member(id):
    member = member_db.get_member(id)
    response_body = {
        "member": member
    }
    return jsonify(response_body), 200

@app.route("/members", methods=['POST']) # add new member
def add_member():
    body = request.get_json()
    member = {
        "first_name": body["first_name"],
        "last_name": member_db.last_name,
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"]
    }
    member_db.add_member(member)
    return jsonify("add_user_ok"), 201

@app.route("/members/<int:id>", methods=['DELETE']) # delete family member
def delete_member(id):
    res = member_db.delete_member(id)

    response_body = {
        "msg": "ok",
        "member": res
    }
    return jsonify(response_body), 200  

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
