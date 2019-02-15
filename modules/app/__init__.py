import os
import json
import datetime
from flask import Flask
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

class JSONEncoder(json.JSONEncoder):
    """ extend json-encoder class"""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)

# add mongo url to flask config, so flask_pymongo can use it to make a conn
app.config['MONGO_URI'] = os.environ.get('DB')
mongo = PyMongo(app)

# use the mod encoder class to handle ObjectId and datetiem obj while jsonifing
# the res
app.json_encoder = JSONEncoder
from app.controllers import *
