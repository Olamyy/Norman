from Norman import utils
from Norman.conversation.adapters import NormanLogicAdapter, NormanInputAdapter


class Norman(object):
    def __init__(self, **kwargs):
        self.user = kwargs.get('user')
        self.logic_adapter = NormanLogicAdapter()
        self.input_adapter = NormanInputAdapter()

        self.initialize()

    def initialize(self):
        pass

    def get_response(self, statement, session_id=None):
        if not session_id:
            session_id = utils.generate_session_id()
        input_statement = self.input_adapter.process_input(statement)

        response = self.generate_response(input_statement)

        return input_statement

    def generate_response(self, input_statement):
        if not input_statement:
            return self.logic_adapter.handle_empty_command(input_statement)
        else:
            pass
