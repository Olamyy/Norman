class Conversation(object):
    def __init__(self, statement=None):
        self.started_at = None
        self.ended_at = None
        self.statement = statement

    # def