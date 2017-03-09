import requests
from flask import Blueprint, jsonify
from flask import json
from flask import make_response
from flask import request
from flask_restful import Resource
from Norman.extensions import csrf_protect

blueprint = Blueprint('web', __name__, url_prefix='/api/web')


@blueprint.route('/register', methods=['GET', 'POST'])
@csrf_protect.exempt
def register():
    view_class = Register()
    if request.method == "GET":
        return view_class.get()
    else:
        return view_class.post()


class Register(Resource):
    def get(self):
        return jsonify({'hello': 'world'})

    def post(self):
        data = request.data.get('name', None)
        print(data)
        return jsonify({'method': 'POST'})

@blueprint.route('/isItUp', methods=['GET', 'POST'])
@csrf_protect.exempt
def isItUp():
    return jsonify({'hello': 'world'})
