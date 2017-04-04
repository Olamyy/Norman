from bson import ObjectId
from mongoengine import DoesNotExist

from Norman.models import User, Hospital


class Utils:

    def get_one(self, id):
        """
        Get a single  instance of a user or hospital
        :param id:
        :return:
        """
        pass

    def get_multiple(self, condition):
        """
        Get multiple instances of user or hospital
        :param condition:
        :return:
        """
        pass

    def update(self, condition):
        """
        Update user or hospital data
        :param condition:
        :return:
        """


class UserUtils(Utils):
    def __init__(self):
        self.userdb = User
        self.id = None
        self.email = None
        self.fb_id = None

    def get_one(self, user_id):
        try:
            user_id = ObjectId(user_id)
            hospital = self.userdb.objects.get(id=user_id)
            if hospital:
                self.id = hospital.id
                self.email = hospital.email
                self.fb_id = hospital.fb
                return self
            else:
                return None
        except DoesNotExist:
                return None


