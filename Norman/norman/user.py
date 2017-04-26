# from Norman.conversation.norman import norman
from datetime import datetime

from Norman.conversation.dbutils import UserUtils
from Norman.conversation.norman import Norman
from Norman.norman import nlp
from Norman.utils import last_five_minute


class NormanUser:
    def __init__(self, fb_id):
        self.fb_id = fb_id
        self.userObj = UserUtils()
        self.first_message = self.userObj.is_first_message(self.fb_id)
        self.instantiated_user = None
        self.session_id = None

    def __str__(self):
        return self.userObj.username

    def __repr__(self):
        return '<NormanUser name:%s>' % self.userObj.username

    def start_conversation(self, message, is_new=False):
        if is_new:
            norman = Norman(user=self.userObj, is_new=True)
            return norman.get_response(message)
        norman = Norman(user=self.userObj, is_new=False)
        return norman.get_response(message, session_id=self.session_id)

    def get_user_instance(self):
        self.session_id = self.userObj

    def get_user_info(self, fb_id=None):
        return self.userObj

    def process_message(self, message, recipient_id):
        global current_user
        if self.first_message:
            return self.handle_first_time_user(recipient_id)
        else:
            current_user = self.userObj.get_one_from_fb_id(recipient_id)

        current_user.last_seen = datetime.strptime(current_user.last_seen ,"%Y-%m-%d %H:%M:%S")
        if current_user.last_seen < last_five_minute:
            self.userObj.update_last_seen(current_user)

        contexts = current_user.contexts
        if message['type'] == 'text':
            if message.lower() == "help":
                return 'getHelp'
            if message[-1] != ".":  # help separate sentence for parsetree
                dotted_message = message + "."
            s = message(dotted_message, relations=True, lemmata=True)
            sentence = s[0]
            nounPhrase = nlp.findNounPhrase(sentence)

    def handle_first_time_user(self, recipient_id):
        pass




