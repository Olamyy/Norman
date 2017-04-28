import datetime

from bson import ObjectId
from mongoengine import DoesNotExist

from Norman.models import UserModel


class UserUtils:
    def __init__(self, recipient_id=None):
        self.userdb = UserModel
        self.is_temp_user = True
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
    
    def get_one_from_fb_id(self, fb_id=None):
        fb_id = self.fb_id if not fb_id else fb_id
        try:
            user = self.userdb.objects.get(fb_id=fb_id)
            if user:
                self.id = user.id
                self.email = user.email
                self.fb_id = user.fb_id
                self.username = user.username
                self.contexts = user.contexts
                return self
        except DoesNotExist:
                return False

    def update(self, match, updates, match_field_name, update_field_name):
        return True if self.userdb.objects.filter(match_field_name=match).update(update_field_name=updates) else False

    def is_first_message(self, fb_id=None):
        fb_id = self.fb_id if not fb_id else fb_id
        try:
            user = self.userdb.objects.get(fb_id=fb_id, has_sent_first_message=False)
            if user:
                return True
        except DoesNotExist:
            return False

    def update_last_seen(self, user):
        now = datetime.datetime.now()
        timestamp = datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
        self.userdb.update({"user_id": user.id}, {"$set": {"last_seen": timestamp}})

    def create_temp_user(self, recipient_id):
        pass

