from datetime import datetime

from flask import Blueprint, jsonify
from flask import request
from flask_excel import ExcelRequest
from flask_restful import Resource

from mongoengine.errors import NotUniqueError

from Norman.extensions import csrf_protect
from Norman.logger import Logger
from Norman.models import Service, Hospital, UserModel
from Norman.utils import generate_id, hash_data
from Norman.utils import Response


blueprint = Blueprint('web', __name__, url_prefix='/api/web')


@blueprint.route('/isItUp', methods=['GET', 'POST'])
@csrf_protect.exempt
def is_it_up():
    test = UserModel(name="Olamilekan", fb_id='HYDSJJ', email='olamyy58222222222222222@gmail.com').save()
    # test = Toga(name="Hello").save()
    if test:
        return jsonify({'hi': 'hello'})
    return ()


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
        action, service_id = data.pop('action', None), data.get('service_id', None)
        if not action:
            return Response.response_error('Unable to handle action', 'No action specified.')
        else:
            if action == "GET":
                return self.get(service_id)
            elif action == "CREATE":
                return self.create_service(data)
            elif action == "UPDATE":
                return self.update_service(data)
            else:
                return self.disable_service(service_id)

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

    def disable_service(self, service_id):
        pass


@blueprint.route('/user', methods=['GET', 'POST'])
@csrf_protect.exempt
def users():
    view_class = UserAPI()
    if request.method == "GET":
        return view_class.get()
    else:
        return view_class.post()


class UserAPI:
    def __init__(self):
        self.user_object = UserModel
        pass

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
                if action == "GET":
                    return self.get(user_id)
                elif action == "CREATE":
                    return self.add_user()
                elif action == "UPDATE":
                    return self.update_user(user_id, data)
                else:
                    # return self.disable_user(user_id)
                    pass
        else:
            data = ExcelRequest(request.environ)
            action = data.form.get('action')
            if action:
                if action == 'CREATE':
                    return self.add_users(data)
            else:
                return Response.response_error('Unable to handle action', 'No action specified.')

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

    def validate_user(self, _id):
        if self.user_object.objects.filter(is_verified=False, fb_id=_id) or not \
                self.user_object.objects.filter(is_verified=False, user_id=_id):
            return False
        else:
            return True

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

        # return response
        # return jsonify({"result": data.get_records(field_name='file')})
        # f = request.files['file']
        # f = excel.ExcelRequest.get_sheet(field_name='file')
        # return excel.
        # data = excel.get_records()
        # Response.response_ok(data)
        # return jsonify({"result": request.get_array(field_name='file')})
        # return jsonify({"result": file.get_records(field_name='file')})
        # print(file_t.get_records(field_name='file'))
        # hospital_id = request.form.get('hospital_id')
        # print('hospital id: ', hospital_id)
        # print('got here!!!!!!!!!!!! ')
        # response = jsonify({"result": file_t.get_records(field_name='file')})
        # print(response)
        # return response

    def add_user(self):
        pass

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

    def post(self):
        data = request.get_json()
        action, hospital_id = data.pop('action', None), data.get('hospital_id', None)
        if not action:
            return Response.response_error('Unable to handle action', 'No action specified.')
        else:
            if action == "GET":
                return self.get_hospital(hospital_id)
            elif action == "CREATE":
                return self.create_hospital(data)
            elif action == "UPDATE":
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
                                   plan_id=data['plan_id'],
                                   password=hashed_password,
                                   tempID=data['temp_id'],
                                   verificationID=generate_id(4),
                                   )
        try:
            create_hospital.save()
            return Response.response_ok(create_hospital)
        except NotUniqueError:
            self.log.log_error('Unable to create hospital')
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
