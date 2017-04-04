from mongoengine import DoesNotExist
from Norman.models import User, Hospital


class NormanUser:
    def __init__(self, user_id):
        self.user = user_id
        if self.isnew():
            self.is_new = True
        self.is_new = False
        self.instantiated_user = None

    def isnew(self):
        try:
            user = Hospital.objects.get()
            print(user.objects.get())
            if user:
                return True
            else:
                return False
        except DoesNotExist:
                return False

    def instantiate_user(self):
        pass

    def start_conversation(self, message, **kwargs):
        pass

    def get_user_instance(self):
        pass


test = NormanUser(user_id='huyr')

print(test)