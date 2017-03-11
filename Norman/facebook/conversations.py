import yaml
from Norman.errors import DeadConversationError
from flask import jsonify


class Conversation:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id', None)
        self.is_alive = True

    def __iter__(self):
        return self

    def __next__(self):
        pass

    def init_conversation(self):
        return True

    def load_conversation(self, conversation_type):
        self.is_alive = True
        with open(conversation_type, 'r') as stream:
            conversation_data = yaml.load(stream)
            print(conversation_data, self.is_alive)
            return conversation_data, self.is_alive


class FreeConversation:
    def __init__(self, **kwargs):
        pass

    def init_conversation(self):
            raise DeadConversationError("The conversation is dead")
