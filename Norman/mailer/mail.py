from flask_mail import Message, Mail


class NormanMailer(Message):
    def __init__(self, recipient):
        super().__init__()
        self.recipient_list = recipient
        self.handle_recipients()

    def handle_recipients(self):
        if isinstance(self.recipient_list, list):
            self.recipients = self.recipient_list
        self.add_recipient(self.recipients)

    def send_mail(self, message):
        pass
