from bson import ObjectId
from mongoengine import DoesNotExist

from Norman.models import User


class Utils:

    def save(self):
        """

        :return:
        """
        pass

    def get_one_from_mongo_id(self, id):
        """
        Get a single  instance of a user or hospital
        :param id:
        :return:
        """
        pass 
    
    def get_one_from_fb_id(self, id):
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

    def update(self,  match,  update):
        """
        Update user or user data
        :param update:
        :param match:
        :return:
        """
        pass


class UserUtils(Utils):
    def __init__(self):
        self.userdb = User
        self.id = None
        self.email = None
        self.fb_id = None

    def get_one_from_mongo_id(self, user_id):
        try:
            user_id = ObjectId(user_id)
            user = self.userdb.objects.get(id=user_id)
            if user:
                self.id = user.id
                self.email = user.email
                self.fb_id = user.fb
                return self
            else:
                return None
        except DoesNotExist:
                return None  
    
    def get_one_from_fb_id(self, fb_id):
        try:
            user = self.userdb.objects.get(fb_id=fb_id)
            if user:
                self.id = user.id
                self.email = user.email
                self.fb_id = user.fb
                return self
            else:
                return None
        except DoesNotExist:
                return None

    def update(self, match, update):
        return True if self.userdb.objects(match).update(update) else False

    def is_first_message(self, fb_id):
        try:
            user = self.userdb.objects.get(fb_id=fb_id, is_first_message=True)
            if user:
                return True
            else:
                return None
        except DoesNotExist:
            return None
