from Norman.core.dbutils import UserUtils
from Norman.utils import generate_session_id
from Norman.conversation.norman import norman


class NormanUser:
    def __init__(self, user_id):
        self.fb_id = user_id
        self.user_db = UserUtils()
        self.is_first = True if self.user_db.is_first_message(self.fb_id) else False
        self.instantiated_user = None
        self.session_id = None
        self.user = self.user_db.get_one_from_fb_id(self.fb_id)

    def instantiate_user(self):
        self.session_id = generate_session_id()
        self.user_db.update({'fb_id': self.user}, {'session_id': self.session_id})
        # User.objects.

    def start_conversation(self, message, **kwargs):
        return norman.get_response(message, self.session_id)

    def get_user_instance(self):
        self.session_id = self.user.id

