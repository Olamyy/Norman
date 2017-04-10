# from Norman.conversation.norman import norman
from Norman.conversation.dbutils import UserUtils
from Norman.conversation.norman import Norman
from Norman.models import UserModel
from Norman.utils import generate_session_id


class NormanUser:
    def __init__(self, user_id):
        self.fb_id = user_id
        self.user_db = UserUtils()
        self.first_message = self.user_db.is_first_message(self.fb_id)
        self.instantiated_user = None
        self.session_id = None
        self.user = self.user_db.get_one_from_fb_id(self.fb_id)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return '<NormanUser name:%s>' % self.user.username

    def instantiate_user(self):
        self.session_id = generate_session_id()
        UserModel.objects.filter(fb_id=self.fb_id).update(session_ids=self.session_id)
        UserModel.objects.filter(fb_id=self.fb_id).update(has_sent_first_message=True)
        self.instantiated_user = True

    def start_conversation(self, message):
        norman = Norman(user=self.user, initialize=True)
        return norman.get_response(message)

    def get_user_instance(self):
        self.session_id = ''

    def get_user_info(self, fb_id=None):
        return self.user


