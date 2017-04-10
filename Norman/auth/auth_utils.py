from flask_login import UserMixin
from mongoengine import DoesNotExist
from Norman.models import Hospital


class HospitalUtil(UserMixin):
    def __init__(self, email=None, password=None, active=True, id=None, name=None):
        self.email = email
        self.password = password
        self.active = active
        self.name = name
        self.isAdmin = False
        self.ver_id = None
        self.id = None

    def validate_email(self, email):
        try:
            hospital = Hospital.objects.get(email=email)
            if hospital:
                self.email = hospital.email
                self.active = hospital.active
                self.password = hospital.password
                self.name = hospital.name
                self.id = hospital.id
                self.ver_id = hospital.ver_id
                return self
            else:
                return None
        except DoesNotExist:
                return None

    def get_mongo_doc(self):
        if self.id:
            return Hospital.objects.with_id(self.id)
        else:
            return None

    def get_by_id(self, user_id):
        hospital = Hospital.objects.with_id(user_id)
        if hospital:
            self.email = hospital.email
            self.active = hospital.active
            self.id = hospital.id
            self.ver_id = hospital.ver_id
            return self
        else:
            return None

    def get_by_verID(self, verID):
        try:
            hospital = Hospital.objects.get(ver_id=verID)
            if hospital:
                self.email = hospital.email
                self.active = hospital.active
                self.password = hospital.password
                self.name = hospital.name
                self.id = hospital.id
                self.ver_id = hospital.ver_id
                return self
            else:
                return None
        except DoesNotExist:
            return None

    def login_user_updates(self, user_id):
        if Hospital.objects.filter(id=user_id).update(is_logged_in=True):
            return True
        else:
            return False

    def logout_user_updates(self, verID):
        if Hospital.objects.filter(ver_id=verID).update(is_logged_in=False):
            return True
        else:
            return False

