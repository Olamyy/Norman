# from Norman.conversation.norman import norman
from Norman.conversation.dbutils import UserUtils


class NormanUser:
    def __init__(self, fb_id):
        self.is_from_ref_id = None
        self.fb_id = fb_id
        self.userObj = UserUtils()
        self.first_message = self.userObj.is_first_message(self.fb_id)
        self.instantiated_user = None
        self.session_id = None

    def get_user_instance(self):
        self.session_id = self.userObj


class TempUser(NormanUser):
    def __init__(self, recipient_id):
        super().__init__(recipient_id)


class MessagingService:
    def __init__(self):
        pass

    def _message(self):
        pass

    def is_valid_message_type(self):
        pass

    @classmethod
    def add_previous_message(cls):
        pass

    def send_notification(self, who, what):
        pass
