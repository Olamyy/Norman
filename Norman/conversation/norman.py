from Norman import utils
from Norman.conversation.adapters import NormanLogicAdapter, NormanInputAdapter
from Norman.norman.user import UserUtils


class Norman(object):
    def __init__(self, **kwargs):
        self.user = kwargs.get('user')
        self.is_new = kwargs.get('is_new', False)
        self.logic_adapter = NormanLogicAdapter()
        self.input_adapter = NormanInputAdapter()
        self.user_utils = UserUtils()
        if self.is_new:
            self.initialize()

    def initialize(self):
            self.load_init_convo()

    def get_response(self, statement, session_id=None):
        if not session_id:
            session_id = utils.generate_session_id()
            self.user_utils.update_session(self.user.id, session_id)
        input_statement = self.input_adapter.process_input(statement)

        response = self.generate_response(input_statement)

        return response

    def generate_response(self, input_statement):
        if not input_statement:
            return self.logic_adapter.handle_empty_command(input_statement)
        else:
            pass
            # self.logic_adapter
            pass

    def load_init_convo(self):
        import yaml
        path = utils.handle_relative_path('Norman/conversation_data/intro_convo.yaml')
        with open('Norman/conversation_data/intro_convo.yaml', 'r') as stream:
            try:
                print(yaml.load(stream))
            except yaml.YAMLError as exc:
                print(exc)
a = Norman()
a.load_init_convo()