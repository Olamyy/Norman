from bson import ObjectId
from flask import jsonify

from Norman.users.models import User


class UserView:
    def __init__(self):
        self.user_object = User
        pass

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

    def validate_user(self, id):
        if self.user_object.objects.filter(is_verified=False, fb_id=id) or not \
                self.user_object.objects.filter(is_verified=False, user_id=id):
            return False
        else:
            return True
