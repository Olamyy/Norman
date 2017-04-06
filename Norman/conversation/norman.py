from chatterbot.chatterbot import ChatBot


class Norman(ChatBot):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.name = name

    def get_response(self, input_item, session_id=None):
        return "Hello World"

norman = Norman(name='Hey')