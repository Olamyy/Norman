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

    def initialize(self):
        if self.is_new:
            self.do_init_convo()

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

    def do_init_convo(self):
        pass
