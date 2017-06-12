from flask import session
from flask_login import UserMixin
from mongoengine import DoesNotExist

from Norman.models import Hospital, Service, UserModel, Notification


class HospitalUtil(UserMixin):
    def __init__(self, email=None, password=None, active=True, name=None, hospital_id=None):
        self.hospital_id = hospital_id
        self.email = email
        self.password = password
        self.active = active
        self.name = name
        self.isAdmin = False
        self.tempID = None
        self.id = None
        self.active = None
        self.has_selected_services = False

    def __repr__(self):
        return self.tempID

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
                self.hospital_id = hospital.hospital_id
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
            session.clear()
            return True
        else:
            return False

    def update_active(self, verificationID):
        return True if Hospital.objects.filter(verificationID=verificationID).update(active=True) else False

    def write_to_session(self, name, value):
        session[name] = value
        return True

    def retrieve_from_session(self, name):
        try:
            data = session[name]
            return data
        except KeyError:
            return False

    def get_current_user_instance(self):
        verification_id = self.retrieve_from_session('current_user')
        hospital = self.get_by_tempID(verification_id)
        return hospital

    def get_all_patients(self, hospital_id):
        try:
            patients = UserModel.objects.filter(hospital_id=hospital_id)
            if patients:
                return patients
            else:
                return None
        except DoesNotExist:
            return None


class PatientUtil(UserMixin):
    def __init__(self, email=None, name=None, user_id=None):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.id = None
        self.drug_use_reminders = None
        self.hospital_id = None
        self.has_hospital = False

    def __repr__(self):
        return self.user_id

    def get_mongo_doc(self):
        if self.id:
            return UserModel.objects.with_id(self.id)
        else:
            return None

    def get_by_id(self, user_id):
        patient = UserModel.objects.with_id(user_id)
        if patient:
            self.email = patient.email
            self.id = patient.id
            self.user_id = patient.id
            self.name = patient.name
            self.drug_use_reminders  = patient.drug_use_reminders
            return self
        else:
            return None

    def get_by_userID(self, user_id):
        patient = UserModel.objects.get(user_id=user_id)
        if patient:
            self.email = patient.email
            self.id = patient.id
            self.user_id = patient.id
            self.name = patient.name
            self.drug_use_reminders  = patient.drug_use_reminders
            return self
        else:
            return None

    def get_by_fbID(self, fb_id):
        patient = UserModel.objects.get(fb_id=fb_id)
        if patient:
            self.email = patient.email
            self.id = patient.id
            self.user_id = patient.id
            self.name = patient.username
            self.hospital_id = patient.hospital_id
            self.drug_use_reminders  = patient.drug_use_reminders
            self.has_hospital = patient.has_hospital
            return self
        else:
            return None

    def login_user_updates(self, user_id):
        if UserModel.objects.filter(id=user_id).update(is_logged_in=True):
            return True
        else:
            return False

    def logout_user_updates(self, verID):
        if UserModel.objects.filter(tempID=verID).update(is_logged_in=False):
            session.clear()
            return True
        else:
            return False

    def update_active(self, verificationID):
        return True if UserModel.objects.filter(verificationID=verificationID).update(active=True) else False

    def write_to_session(self, name, value):
        session[name] = value
        return True

    def retrieve_from_session(self, name):
        try:
            data = session[name]
            return data
        except KeyError:
            return False

    def get_current_user_instance(self):
        verification_id = self.retrieve_from_session('current_user')
        hospital = self.get_by_userID(verification_id)
        return hospital

    def get_all_patients(self, hospital_id):
        try:
            patients = UserModel.objects.filter(hospital_id=hospital_id)
            if patients:
                return patients
            else:
                return None
        except DoesNotExist:
            return None

    def validate_email(self, email):
        try:
            patient = UserModel.objects.get(email=email)
            if patient:
                self.email = patient.email
                self.id = patient.id
                self.user_id = patient.id
                self.name = patient.name
                self.drug_use_reminders = patient.drug_use_reminders
                return self
            else:
                return None
        except DoesNotExist:
            return None

    def update_password(self, user_id, password):
        return


class ServiceUtil:
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


class NotificationUtil:
    def __init__(self, hospital_id=None, fb_id=None):
        self.message = None
        self.sender_id = None
        self.hospital_id = hospital_id
        self.fb_id = fb_id

    def get_all_notification(self):
        if self.hospital_id:
            query = Notification.objects.get(hospital_id=self.hospital_id)
            if query:
                return query
            else:
                return False
        query = Notification.objects.get(fb_id=self.fb_id)
        if query:
            return query
        else:
            return False
