from bson import ObjectId
from mongoengine import DoesNotExist

from Norman.models import UserModel


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

    def update(self,  match,  update, match_field_name, update_field_name):
        """
        Update user or user data
        :param update_field_name:
        :param match_field_name:
        :param update:
        :param match:
        :return:
        """
        pass


class UserUtils(Utils):
    def __init__(self):
        self.userdb = UserModel
        self.id = None
        self.email = None
        self.fb_id = None
        self.username = None

    def get_one_from_mongo_id(self, user_id):
        try:
            user_id = ObjectId(user_id)
            user = self.userdb.objects.get(id=user_id)
            if user:
                self.id = user.id
                self.email = user.email
                self.fb_id = user.fb_id
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
                self.fb_id = user.fb_id
                self.username = user.username
                return self
        except DoesNotExist:
                return False

    def update(self, match, updates, match_field_name, update_field_name):
        return True if self.userdb.objects.filter(match_field_name=match).update(update_field_name=updates) else False

    def is_first_message(self, fb_id):
        try:
            user = self.userdb.objects.get(fb_id=fb_id, has_sent_first_message=True)
            if user:
                return True
        except DoesNotExist:
            return False

    def update_session(self, user_id, session_id):
        pass

    def update_session_with_fb_id(self, fb_id, session_id):
        pass

    def update_first_message(self, fb_id):
        pass
