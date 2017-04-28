# from Norman.conversation.norman import norman
from Norman.conversation.dbutils import UserUtils
from Norman.norman.nlp import NLPProcessor


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

    def process_message(self, message, recipient_id):
        global current_user
        current_user = self.userObj.get_one_from_fb_id(recipient_id)
        # current_user.last_seen = datetime.strptime(current_user.last_seen ,"%Y-%m-%d %H:%M:%S")
        # if current_user.last_seen < last_five_minute:
        #     self.userObj.update_last_seen(current_user)
        #     pass
        #     print("I'm back here.")

        contexts = current_user.context
        if message['type'] == 'text':
            message_text = message['data'].decode("utf-8")
            if message_text.lower() == "help":
                return 'getHelp'
            if message_text[-1] != ".":  # help separate sentence for parsetree
                dotted_message = message_text + "."
                return NLPProcessor(dotted_message)

    def handle_first_time_user(self, recipient_id):
        pass

    def create_temp_user(self, recipient_id):
        pass

    def getuserContext(self):
        pass

    def popContexts(self, context):
        pass

    def handle_find_food(self, user_id, context, sentence, nounPhrase, message, message_text):
        pass

    def handle_yelp_rename(self, user_id, user, context, message_text):
        pass

    def handleUncategorized(self, user_id, message_text):
        pass


class TempUser(NormanUser):
    def __init__(self, recipient_id):
        super().__init__(recipient_id)



