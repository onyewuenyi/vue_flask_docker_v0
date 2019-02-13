"""
    controller and routes for users
    gen query: .db.<collection>.<query>
    - <query>: ‘find’, ‘update’, ‘delete’
"""
import os
from flask import request, jsonify
from app import app mongo
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/user', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():
    """
    register a route with GET, POST, DELETE & PATCH methods
    """
    def get():
        query = request.args
        data = mongo.db.users.find_one(query)
        return jsonify(data), 200

    def post():
        data = request.get_json()
        if data.get('name') is not None and data.get('email') is not None:
            mongo.db.users.insert_one(data)
            return jsonfiy({'ok: True', 'message:'})
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    def delete():
        data = request.get_json()
        if data.get('email') is not None:
            db_response = mongo.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': False, 'message': 'no record found'}
            return jsonify(reponse), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    def patch():
        data = request.get_json()
        if data.get('query') != {}:
            mongo.db.users.update_one(
                data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'GET':
        get()
    else if request.method == 'POST':
        post()
    else if request.method == 'DELETE':
        delete()
    else if request.method == 'PATCH':
        patch()
