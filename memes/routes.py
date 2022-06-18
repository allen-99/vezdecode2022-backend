from flask import Blueprint, jsonify, request, session
from db import mongo
import requests
import json
from bson.objectid import ObjectId

routes = Blueprint('routes', __name__)
db = mongo.db


@routes.route('/get_all_memes', methods=['GET'])
def hello():


