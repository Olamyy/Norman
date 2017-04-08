
class Conversation(object):
    def __init__(self, statement=None):
        self.started_at = None
        self.ended_at = None
        self.statement = statement
        self.is_alive = None
        self.base_flow = []
        self.conversation_storage_handler = None
        self.extra_data = {}

    def is_alive(self):
        return True if self.is_alive else False

    def save(self):
        """
        Save a conversation response as a key value pair to aid retrieval
        :return:
        """
        self.conversation_storage_handler.update(self)

    def add_extra_data(self, key, value):
        self.extra_data[key] = value

    def add_response(self):
        """

        :return:
        """
        pass

    def adapter_response(self):
        """

        :return:
        """
        pass
    

class CommandConversation(Conversation):
    pass


class EmptyCommandConversation(CommandConversation):
    pass


