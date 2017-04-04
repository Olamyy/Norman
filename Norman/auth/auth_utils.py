from flask_login import UserMixin
from mongoengine import DoesNotExist

from Norman.models import Hospital, User


class HospitalUtil(UserMixin):
    def __init__(self, email=None, password=None, active=True, id=None, name=None):
        self.email = email
        self.password = password
        self.active = active
        self.name = name
        self.isAdmin = False
        self.id = None
    
    def get_by_email(self, email):
        hospital = Hospital.objects.get(email=email)
        if hospital:
            self.email = hospital.email
            self.active = hospital.active
            self.id = hospital.id
            return self
        else:
            return None

    def get_by_email_w_password(self, email):
        try:
            hospital = Hospital.objects.get(email=email)
            if hospital:
                self.email = hospital.email
                self.active = hospital.active
                self.password = hospital.password
                self.name = hospital.name
                self.id = hospital.id
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

    def get_by_id(self, id):
        hospital = Hospital.objects.with_id(id)
        if hospital:
            self.email = hospital.email
            self.active = hospital.active
            self.id = hospital.id
    
            return self
        else:
            return None