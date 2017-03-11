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


class FreeConversation(Conversation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def init_conversation(self):
        if not self.is_alive:
            raise DeadConversationError("The conversation is dead")
        else:
            conversation = self.load_conversation(
                '/home/lekanterragon/Desktop/Norman/Norman/conversation_data/free_conversation.yaml')
            conversation_data, self.is_alive = conversation[0], conversation[1]

            return jsonify({'response': conversation_data['base_message']})
