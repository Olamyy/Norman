from flask_login import UserMixin
from mongoengine import DoesNotExist
from Norman.models import Hospital, Service


class HospitalUtil(UserMixin):
    def __init__(self, email=None, password=None, active=True, id=None, name=None):
        self.email = email
        self.password = password
        self.active = active
        self.name = name
        self.isAdmin = False
        self.tempID = None
        self.id = None
        self.active = None
        self.has_selected_services = False

    def validate_email(self, email):
        try:
            hospital = Hospital.objects.get(email=email)
            if hospital:
                self.email = hospital.email
                self.active = hospital.active
                self.password = hospital.password
                self.name = hospital.name
                self.id = hospital.id
                self.tempID = hospital.tempID
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
            self.tempID = hospital.tempID
            return self
        else:
            return None

    def get_by_tempID(self, tempID):
        try:
            hospital = Hospital.objects.get(tempID=tempID)
            if hospital:
                self.email = hospital.email
                self.active = hospital.active
                self.password = hospital.password
                self.name = hospital.name
                self.id = hospital.id
                self.tempID = hospital.tempID
                self.has_selected_services = hospital.has_selected_services
                return self
            else:
                return None
        except DoesNotExist:
            return None

    def get_by_verID(self, verification_id):
        try:
            hospital = Hospital.objects.get(verificationID=verification_id)
            if hospital:
                self.email = hospital.email
                self.active = hospital.active
                self.password = hospital.password
                self.name = hospital.name
                self.id = hospital.id
                self.tempID = hospital.tempID
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
        if Hospital.objects.filter(tempID=verID).update(is_logged_in=False):
            return True
        else:
            return False

    def update_active(self, verificationID):
        return True if Hospital.objects.filter(verificationID=verificationID).update(active=True) else False


class ServiceUtil(UserMixin):
    def __init__(self):
        self.name = None
        self.long_description = None
        self.short_description = False
        self.service_id = None

    def get_by_id(self, user_id):
        service = Service.objects.with_id(user_id)
        if service:
            self.name = service.name
            self.long_description = service.long_description
            self.short_description = service.short_description
            self.service_id = service.service_id
            return self
        else:
            return None

    def get_all_services(self):
        services = Service.objects.all()
        if services:
            return services
        else:
            return False