
class Command(object):
    def __init__(self, statement=None):
        self.command_marker = 'do:'
        self.statement = statement
        self.is_normal_message = False

    def __str__(self):
        return self.statement

    def __repr__(self):
        return '<Command statement:%s>' % self.statement

    def __hash__(self):
        return hash(self.statement)

    def is_valid_command(self, statement):
        self.statement = statement
        if self.command_marker in statement:
            return True
        return False

    def get_command_statement(self):
        return self._strip_message(self.statement)

    @staticmethod
    def _strip_message(statement):
        return str(statement).replace('do:', '')

    def process_command(self, command_statement):
        statement = self._strip_message(command_statement)
        if not statement:
            return statement
        else:
            return "Empty Statement"


class NormalMessage(object):
    def __init__(self, statement=None):
        self.is_command = False

    def is_valid_message(self, statement):
        pass


class ServiceResponse:
    def __init__(self, statement):
        self.statement = statement

    def __str__(self):
        return self.statement

    def __repr__(self):
        return '<ServiceResponse statement:%s>' % self.statement

    def __hash__(self):
        return hash(self.statement)


