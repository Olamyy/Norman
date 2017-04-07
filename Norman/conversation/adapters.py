from __future__ import unicode_literals

from chatterbot.adapters import Adapter
from chatterbot.logic import LogicAdapter

from Norman.conversation.message_types import Command, NormalMessage, ServiceResponse


class InputAdapter(Adapter):
    """
    This is an abstract class that represents the
    interface that all input adapters should implement.
    """

    def process_input(self, *args, **kwargs):
        """
        Returns a statement object based on the input source.
        """
        raise self.AdapterMethodNotImplementedError()

    def process_input_statement(self, *args, **kwargs):
        """
        Return an existing statement object (if one exists).
        """
        input_statement = self.process_input(*args, **kwargs)
        self.logger.info('Recieved input statement: {}'.format(input_statement.text))

        existing_statement = self.chatbot.storage.find(input_statement.text)

        if existing_statement:
            self.logger.info('"{}" is a known statement'.format(input_statement.text))
            input_statement = existing_statement
        else:
            self.logger.info('"{}" is not a known statement'.format(input_statement.text))

        return input_statement


class NormanInputAdapter(InputAdapter):
    def __init__(self, **kwargs):
        super(NormanInputAdapter, self).__init__(**kwargs)
        self.recipient = kwargs.get('recipient_id')
        self.command_obj = Command()
        self.normal_message_obj = NormalMessage()

    def detect_input_type(self, statement):
        if self.command_obj.is_valid_command(statement):
            return Command(statement)
        elif self.normal_message_obj.is_valid_message(statement):
            return NormalMessage(statement)
        else:
            return ServiceResponse(statement)

    def process_input(self, statement):
        statement = self.detect_input_type(statement)
        if isinstance(statement, Command):
            return statement.process_command(statement)
        elif isinstance(statement, NormalMessage):
            pass
        else:
            pass


class NormanLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(NormanLogicAdapter, self).__init__(**kwargs)
        self.recipient = kwargs.get('recipient_id')
        self.command_obj = Command()
        self.command = 'command'
        self.normal_message = 'normal'

    def detect_input_type(self, statement):
        if self.command_obj.is_valid_command(statement):
            return self.command
        else:
            return self.normal_message

    def process_input(self, statement):
        input_type = self.detect_input_type(statement)
        return statement


class NormanStorageAdapter(LogicAdapter):
    pass


class NormanOutputAdapter(LogicAdapter):
    pass
