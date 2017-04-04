
from bson import ObjectId, errors
from flask import Blueprint, jsonify
from flask import request
from flask_restful import Resource
from Norman.models import Service, Hospital, User
from Norman.extensions import csrf_protect, db
from Norman.utils import Response as response
from Norman.utils import generate_id
from datetime import datetime
from mongoengine.errors import NotUniqueError

blueprint = Blueprint('web', __name__, url_prefix='/api/web')


@blueprint.route('/isItUp', methods=['GET', 'POST'])
@csrf_protect.exempt
def isItUp():
    return jsonify({'hello': 'world'})


@blueprint.route('/hospital', methods=['GET', 'POST'])
@csrf_protect.exempt
def register():
    view_class = HospitalApi()
    if request.method == "GET":
        return view_class.get_hospital()
    else:
        return view_class.post()


class ServiceAPI(Resource):
    def get(self, service_id=None):
        service_id = request.args.get('service_id', service_id)
        service_details = Service.objects.filter(service_id=service_id)
        if not service_details:
            return response.response_error("Unable to retrieve service", "Invalid Service ID")
        else:
            return response.response_ok(service_details)

    def post(self):
        data = request.get_json()
        action, service_id = data.get('action', None), data.get('service_id', None)
        if not action:
            return response.response_error('Unable to handle action', 'No action specified.')
        else:
            if action == "GET":
                return self.get(service_id)
            elif action == "CREATE":
                return self.create_service(data)
            else:
                return self.disable_service(service_id)

    def create_service(self, data):
        create_service = Service(name=data['name'],
                                 long_description=data['long_description'],
                                 created_at=datetime.now(),
                                 short_description=data['short_description'],
                                 service_id=generate_id(10))
        try:
            create_service.save()
            return response.response_ok(create_service)
        except NotUniqueError:
            return response.response_error('Unable to create service', 'Service name already exists')

    def disable_service(self, service_id):
        pass


class UserAPI:
    def __init__(self):
        self.user_object = User
        pass

    def validate_fb_id(self, fb_id):
        if not self.user_object.objects.get(fb_id=fb_id):
            return False
        else:
            return True

    def validate_user_id(self, user_id):
        if not self.user_object.objects.filter(username=user_id):
            return False
        else:
            return True

    def validate_user(self, id):
        if self.user_object.objects.filter(is_verified=False, fb_id=id) or not \
                self.user_object.objects.filter(is_verified=False, user_id=id):
            return False
        else:
            return True


class HospitalApi(Resource):
    def post(self):
        data = request.get_json()
        action, hospital_id = data.get('action', '').lower(), data.get('hospital_id', None)
        if not action:
            return response.response_error('Unable to handle action', 'No action specified.')
        else:
            if action == "get":
                return self.get_hospital(hospital_id)
            elif action == "create":
                return self.create_hospital(data)
            elif action == "update":
                return self.update_hospital(hospital_id)
            return self.disable_hospital(hospital_id)

    def get_hospital(self, hospital_id=None):
        try:
            hospital_details = db.find_one({"_id": ObjectId(hospital_id)})
            if not hospital_details:
                return response.response_error("Unable to retrieve Hospital", "Invalid Hospital ID")
            else:
                return response.response_ok(hospital_details)
        except errors.InvalidId as error:
            return response.response_error("Unable to retrieve Hospital", error)

    def create_hospital(self, data):
        create_hospital = Hospital(name=data['name'],
                                   email=data['email'],
                                   reg_num=data['reg_num'],
                                   created_at=datetime.now(),
                                   plan_id=data['plan_id'],
                                   password=data['password'],
                                   )
        try:
            create_hospital.save()
            return response.response_ok(create_hospital)
        except NotUniqueError:
            return response.response_error('Unable to create service', 'Hospital name already exists')

    def disable_hospital(self, hospital_id):
        pass

    def update_hospital(self, hospital_id):
        pass