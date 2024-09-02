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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# list all members of the family
@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# list just one member of the family
@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    try:
        one_member = jackson_family.get_member(id)
        return jsonify({"done": "Member found"}, one_member), 200
    except:
        return jsonify({"error": "Member not found"}), 400

# add one member to the family
@app.route('/member', methods=['POST'])
def add_one_member():
    try:
        reques_json = request.json
        new_member = jackson_family.add_member(reques_json)
        return jsonify({"done": "Member added"})
    except:
        return jsonify({"error": "Member could not be added"},new_member)

# delete one member of the family
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_one_member(id):
    try:
        member_to_delete = jackson_family.delete_member(id)
        return jsonify({"done": "Member removed"}, member_to_delete), 200
    except:
        return jsonify({"error": "Member not found"}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
