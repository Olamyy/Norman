# from Norman.conversation.norman import norman
from Norman.conversation.dbutils import UserUtils
from Norman.conversation.norman import Norman
from Norman.utils import generate_session_id


class NormanUser:
    def __init__(self, fb_id):
        self.fb_id = fb_id
        self.user_utils = UserUtils()
        self.first_message = self.user_utils.is_first_message(self.fb_id)
        self.instantiated_user = None
        self.session_id = None
        self.user = self.user_utils.get_one_from_fb_id(self.fb_id)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return '<NormanUser name:%s>' % self.user.username

    def instantiate_user(self):
        self.session_id = generate_session_id()
        self.user_utils.update_session_with_fb_id(self.fb_id, self.session_id)
        self.user_utils.update_first_message(self.fb_id)
        self.instantiated_user = True

    def start_conversation(self, message, is_new=False):
        if is_new:
            norman = Norman(user=self.user, is_new=True)
            return norman.get_response(message)
        norman = Norman(user=self.user, is_new=False)
        return norman.get_response(message, session_id=self.session_id)

    def get_user_instance(self):
        self.session_id = self.user

    def get_user_info(self, fb_id=None):
        return self.user


