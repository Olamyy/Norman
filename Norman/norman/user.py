# from Norman.conversation.norman import norman
from datetime import datetime

from Norman.conversation.dbutils import UserUtils
from Norman.conversation.norman import Norman
from Norman.utils import last_five_minute


class NormanUser:
    def __init__(self, fb_id):
        self.fb_id = fb_id
        self.first_message = UserUtils(self.fb_id).is_first_message()
        self.instantiated_user = None
        self.session_id = None
        self.user = UserUtils(self.fb_id).get_one_from_fb_id()

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return '<NormanUser name:%s>' % self.user.username

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

    def process_message(self, message, recipient_id):
        global current_user
        if self.user.is_new_user(recipient_id):
            pass
        else:
            current_user = self.user.get_one_from_fb_id()

        current_user.last_seen = datetime.strptime(current_user.last_seen ,"%Y-%m-%d %H:%M:%S")
        if current_user.last_seen < last_five_minute:
            self.user.update_last_seen()

        contexts = current_user.contexts




