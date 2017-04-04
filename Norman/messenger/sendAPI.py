from flask import jsonify
from Norman.settings import FBConfig
from Norman.api.base import base
from Norman.errors import HttpError


# Buttons
# Quick Replies
# Sender Actions
# Upload API
# Error Codes

class SendAPI:
    def __init__(self, payload):
        self.graphAPIURL = FBConfig.GRAPH_API_URL.replace('<action>', '/me/messages?')

    def send_message(self, payload):
        request = base.exec_request('POST', self.graphAPIURL, data=payload)
        if request:
            print(request)
        else:
            raise HttpError('Unable to complete request.')


class Payload:
    def __init__(self, recipient, message=None, sender_action=None, notification_type="REGULAR"):
        """

        :param recipient:
        :param message:
        :param sender_action:
        :param notification_type:
        """
        self.recipient = recipient
        if not message and not sender_action:
            raise ValueError("At least one of message/sender is required ")

        self.payload = jsonify(
            {
                "recipient": {"id": self.recipient.user_id},
                "message": {message.content},
                "sender_action": sender_action,
                "notification_type": notification_type
            }
        )


message = {}


class Message:
    def __init__(self, text, attachment=False, quick_replies=False, metadata=None):
        self.content = {
            "text": text,
            "attachment": attachment,
            "quick_replies": quick_replies,
            "metadata": metadata
        }
        self.message = message
        self.text = None
        self.attachment = None
        self.quick_replies = None
        self.metadata = None

    def clean_message(self):
        self.text = self.clean_text(message['text'])
        self.attachment = message['text']
        self.quick_replies = message['text']
        self.metadata = message['text']

        return self

    def clean_text(self, param):
        return True


class Recipient:
    def __init__(self, user_id):
        self.user_id = user_id
