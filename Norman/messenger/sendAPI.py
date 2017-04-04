from flask import jsonify
from Norman.settings import Config
from Norman.api.base import base
from Norman.errors import HttpError


# Buttons
# Quick Replies
# Sender Actions
# Upload API
# Error Codes

class SendAPI:
    def __init__(self):
        self.graphAPIURL = Config.GRAPH_API_URL.replace('<action>', '/me/messages?')

    def send_message(self, payload):
        request = base.exec_request('POST', self.graphAPIURL, data=payload)
        if request:
            print(request)
        else:
            raise HttpError('Unable to complete request.')


class Payload:
    def __init__(self, recipient, message=None, sender_action=None, notification_type="REGULAR"):
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


class Message:
    def __init__(self, text, attachment=False, quick_replies=False, metadata=None):
        self.content = {
            "text": text,
            "attachment": attachment,
            "quick_replies": quick_replies,
            "metadata": metadata
        }


class Recipient:
    def __init__(self, user_id):
        self.user_id = user_id
