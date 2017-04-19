class NormanService(object):
    def __init__(self, norman_user):
        self.name = None
        self.user = norman_user

    def __repr__(self):
        return '<NormanService name:%s>' % self.name

    def __str__(self):
        return self.name

    def initialize(self):
        pass

    @staticmethod
    def getQuestions():
        pass

    def logResponse(self, response, **kwargs):
        pass


class ReminderService(NormanService):
    def __init__(self, norman_user):
        super().__init__(norman_user)

