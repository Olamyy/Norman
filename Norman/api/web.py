from datetime import datetime

from flask import Blueprint, jsonify
from flask import request
from flask_excel import ExcelRequest
from flask_restful import Resource
from mongoengine.errors import NotUniqueError
from Norman.auth.auth_utils import HospitalUtil
from Norman.extensions import csrf_protect
from Norman.logger import Logger
from Norman.models import Service, Hospital, UserModel
from Norman.utils import generate_id, hash_data
from Norman.utils import Response
from Norman.models import Service
from Norman.models import Service, Hospital, User
from Norman.extensions import csrf_protect
from Norman.utils import Response as response
from Norman.utils import generate_id
from datetime import datetime
from mongoengine.errors import NotUniqueError
from Norman.settings import DevConfig


blueprint = Blueprint('web', __name__, url_prefix='/api/web')
db = DevConfig.pymongo_client.Norman['hospital']
print(db)


blueprint = Blueprint('web', __name__, url_prefix='/api/web')


@blueprint.route('/service', methods=['GET', 'POST'])
@csrf_protect.exempt
def register_service():
    view_class = ServiceAPI()
    if request.method == "GET":
        return view_class.get()
    else:
        return view_class.post()


class ServiceAPI(Resource):
    @staticmethod
    def get(service_id=None):
        service_id = request.args.get('service_id', service_id)
        service_details = Service.objects.filter(service_id=service_id)
        if not service_details:
            return Response.response_error("Unable to retrieve service", "Invalid Service ID")
        else:
            return Response.response_ok(service_details)

    def post(self):
        data = request.get_json()
        if data:
            action, service_id = data.pop('action', None), data.get('service_id', None)
            if not action:
                return Response.response_error('Unable to handle action', 'No action specified.')
        action, service_id = data.get('action', None).lower(), data.get('service_id', None)
        if not action:
            return response.response_error('Unable to handle action', 'No action specified.')
        else:
            if action == "get":
                return self.get(service_id)
            elif action == "create":
                return self.create_service(data)
            else:
                if action == "GET":
                    return self.get(service_id)
                elif action == "CREATE":
                    return self.create_service(data)
                elif action == "UPDATE":
                    return self.update_service(data)
                else:
                    return Response.response_error('Unable to handle action', 'Invalid action.')
        else:
            data = ExcelRequest(request.environ)
            self.add_questions(data)

    @staticmethod
    def create_service(data):
        create_service = Service(name=data['name'],
                                 long_description=data['long_description'],
                                 created_at=datetime.now(),
                                 short_description=data['short_description'],
                                 questions=data.get('questions', []),
                                 service_id=generate_id(10))
        try:
            create_service.save()
            return Response.response_ok(create_service)
        except NotUniqueError:
            return Response.response_error('Unable to create service', 'Service name already exists')

    @staticmethod
    def update_service(data):
        service_id = data.pop('service_id', None)
        service_details = Service.objects.filter(service_id=service_id)
        if not service_details:
            return Response.response_error("Unable to retrieve service", "Invalid Service ID")
        else:
            questions = data.pop('questions', None)
            if questions:
                Service.objects(service_id=service_id).update(add_to_set__questions=questions)
            Service.objects(service_id=service_id).update(**data)
            return Response.response_ok(service_details)

    @staticmethod
    def add_questions(data):
        service_id = data.form.get('service_id')
        questions = data.get_array(field_name='file')
        service_details = Service.objects.filter(service_id=service_id)
        Service.objects(service_id=service_id).update(add_to_set__questions=questions)
        return Response.response_ok(service_details)


@blueprint.route('/user', methods=['GET', 'POST'])
@csrf_protect.exempt
def users():
    view_class = UserAPI()
    if request.method == "GET":
        return view_class.get()
    else:
        return view_class.post()


# <<<<<<< HEAD
# @blueprint.route('/hospital', methods=['POST'])
# @csrf_protect.exempt
# def hospital_api():
#     view_class = HospitalApi()
#     if request.method == "POST":
#         return view_class.post()


# class HospitalApi(Resource):
#     def post(self):
#         data = request.get_json()
#         action, hospital_id = data.get('action', None).lower(), data.get('hospital_id', None)
#         if not action:
#             return response.response_error('Unable to handle action', 'No action specified.')
#         else:
#             if action == "get":
#                 return self.get_hospital(hospital_id)
#             elif action == "create":
#                 return self.create_hospital(data)
#             else:
#                 return self.disable_service(hospital_id)

#     def get_hospital(self, hospital_id=None):
#         try:
#             hospital_details = db.find_one({"_id": ObjectId(hospital_id)})
#             print(hospital_details)
#             if not hospital_details:
#                 return response.response_error("Unable to retrieve Hospital", "Invalid Hospital ID")
#             else:
#                 return response.response_ok(hospital_details)
#         except errors.InvalidId as error:
#             return response.response_error("Unable to retrieve Hospital", error)

#     def create_hospital(self, data):
#         create_hospital = Hospital(name=data['name'],
#                                    address=data['address'],
#                                    specialty=data['specialty'],
#                                    email=data['email'],
#                                    created_at=datetime.now(),
#                                    plan_id=data['plan_id'],
#                                    description=data['description'], active=False)
#         try:
#             create_hospital.save()
#             return response.response_ok(create_hospital)
#         except NotUniqueError:
#             return response.response_error('Unable to create service', 'Hospital name already exists')

#     def disable_hospital(self, service_id):
#         pass


# @blueprint.route('/user', methods=['POST'])
# @csrf_protect.exempt
# def user_api():
#     view_class = UserApi()
#     if request.method == "POST":
#         return view_class.post()


# class UserApi(Resource):
#     def post(self):
#         data = request.get_json()
#         action, user_id = data.get('action', None).lower(), data.get('user_id', None)
#         if not action:
#             return response.response_error('Unable to handle action', 'No action specified.')
#         else:
#             if action == "get":
#                 return self.get_user(user_id)
#             elif action == "create":
#                 return self.create_user(data)
#             else:
#                 return self.disable_user(user_id)

#     def get_user(self, user_id=None):
#         try:
#             user_details = User.objects.filter(_id=ObjectId(user_id))
#             if not user_details:
#                 return response.response_error("Unable to retrieve user", "Invalid User ID")
#             else:
#                 return response.response_ok(user_details)
#         except errors.InvalidId as error:
#             return response.response_error("Unable to retrieve user", error)

#     def create_user(self, data):
#         create_user = User(name=data['name'], password=data['password'],
#                                    address=data['address'], specialty=data['specialty'], email=data['email'], created_at=datetime.now(),
#                                    plan_id=data['plan_id'], description=data['description'],
#                                    service_list=data['service_list'].split(','), active=False)
#         try:
#             create_user.save()
#             return response.response_ok(create_user)
#         except NotUniqueError:
#             return response.response_error('Unable to create user', 'User already exists')

#     def disable_user(self, service_id):
#         pass
# =======
class UserAPI:
    def __init__(self):
        self.user_object = UserModel

    def get(self, user_id=None):
        user_id = request.args.get('user_id', user_id)
        user_details = self.user_object.objects.filter(user_id=user_id)
        if not user_details:
            return Response.response_error("Unable to retrieve user", "Invalid USER ID")
        else:
            return Response.response_ok(user_details)

    def post(self):
        data = request.get_json()
        if data:
            action, user_id = data.pop('action', None), data.get('user_id', None)
            if not action:
                return Response.response_error('Unable to handle action', 'No action specified.')
            else:
                if action.upper() == "GET":
                    return self.get(user_id)
                elif action.upper() == "CREATE":
                    return self.add_user(data)
                elif action.upper() == "UPDATE":
                    return self.update_user(user_id, data)
                else:
                    return Response.response_error('Unable to handle action', 'Invalid action')
        else:
            data = ExcelRequest(request.environ)
            action = data.form.get('action')
            if action:
                if action.upper() == 'CREATE':
                    return self.add_users(data)
            else:
                return Response.response_error('Unable to handle action', 'No action specified.')

    @staticmethod
    def add_users(data):
        hospital_id = data.form.get('hospital_id')
        user_records = data.get_records(field_name='file')
        entries = []
        for user in user_records:
            new_user = UserModel(first_name=user['First Name'], last_name=user['Last Name'],
                                 email=user['Email'], hospital_id=hospital_id, user_id=generate_id(10))
            new_user.save()
            entries.append(new_user)
        return Response.response_ok(entries)

    @staticmethod
    def add_user(data):
        data['user_id'] = generate_id(10)
        user_details = UserModel(**data)
        try:
            if user_details.save():
                # @Todo: Handle Link Generation and Patient Email Handling here
                pass
        except NotUniqueError as e:
            return Response.response_error('Unable to add user', str(e))
        return Response.response_ok(user_details)

    def update_user(self, user_id, data):
        user_details = self.user_object.objects.filter(user_id=user_id)
        if not user_details:
            return Response.response_error("Unable to retrieve user, Invalid USER ID")
        else:
            self.user_object.objects(user_id=user_id).update(**data)
            return Response.response_ok(user_details)


@blueprint.route('/hospital', methods=['GET', 'POST'])
@csrf_protect.exempt
def register_hospital():
    view_class = HospitalApi()
    if request.method == "GET":
        return view_class.get_hospital()
    else:
        return view_class.post()

class HospitalApi(Resource):
    def __init__(self):
        self.log = Logger()
        self.hospital_util = HospitalUtil()

    def post(self):
        data = request.get_json()
        action, hospital_id = data.pop('action', None), data.get('hospital_id', None)
        if not action:
            return Response.response_error('Unable to handle action', 'No action specified.')
        else:
            if action.upper() == "GET":
                return self.get_hospital(hospital_id)
            elif action.upper() == "CREATE":
                return self.create_hospital(data)
            elif action.upper() == "UPDATE":
                return self.update_hospital(hospital_id, data)

    @staticmethod
    def get_hospital(hospital_id=None):
        if not hospital_id:
            return Response.response_error("Unable to retrieve Hospital", "Invalid Hospital ID")
        else:
            hospital_details = Hospital.objects.filter(hospital_id=hospital_id)
            return Response.response_ok(hospital_details)

    def create_hospital(self, data):
        hashed_password = hash_data(data['password'])
        create_hospital = Hospital(name=data['name'],
                                   email=data['email'],
                                   reg_num=data['reg_num'],
                                   created_at=datetime.now(),
                                   hospital_id=generate_id(10),
                                   password=hashed_password,
                                   tempID=data['temp_id'],
                                   verificationID=generate_id(4),
                                   )
        try:
            if create_hospital.save():
                self.hospital_util.write_to_session('current_user', data['temp_id'])
                return Response.response_ok(create_hospital)
        except NotUniqueError:
            # self.log.log_error('Unable to create hospital')
            return Response.response_error('Unable to create hospital', 'Hospital already exists')

    @staticmethod
    def disable_hospital(hospital_id):
        hospital_details = Hospital.objects.filter(hospital_id=hospital_id)
        if not hospital_details:
            return Response.response_error("Unable to retrieve hospital", "Invalid Hospital ID")
        else:
            Hospital.objects(hospital_id=hospital_id).update(disabled=True)

    @staticmethod
    def update_hospital(hospital_id, data):
        hospital_details = Hospital.objects.filter(hospital_id=hospital_id)
        if not hospital_details:
            return Response.response_error("Unable to retrieve hospital", "Invalid Hospital ID")
        else:
            Hospital.objects(hospital_id=hospital_id).update(**data)
            return Response.response_ok(hospital_details)
