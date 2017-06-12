from Norman.messenger.sendAPI import PostBackMessages


class PayloadConversationHandler:
    def __init__(self, **kwargs):
        self.registered = kwargs.get('registered')
        self.recipient_id = kwargs.get('recipient_id')
    
    def handleconversation(self, postback_payload):
        postbackmessages = PostBackMessages(self.recipient_id)
        if self.registered:
            if postback_payload == 'NORMAN_GET_HELP':
                return postbackmessages.handle_help(self.registered)
            elif postback_payload == 'NORMAN_GET_STARTED_PAYLOAD':
                return postbackmessages.handle_get_started(self.registered)
            elif postback_payload == 'NORMAN_GET_STARTED_MEANING':
                return postbackmessages.handle_get_started_meaning(self.registered)
            elif postback_payload == 'NORMAN_GET_STARTED_HOW':
                return postbackmessages.handle_get_started_how(self.registered)
            elif postback_payload == 'NORMAN_GET_ALL_SERVICE_LIST':
                return postbackmessages.get_started_service_list(self.registered)
            elif postback_payload == 'GOOD_TO_GO':
                return postbackmessages.good_to_go(self.registered)
            elif postback_payload == 'GOOD_TO_GO_FREE':
                return postbackmessages.good_to_go_free(self.registered)
        else:
            pass