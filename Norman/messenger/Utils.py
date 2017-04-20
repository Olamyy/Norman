from flask import json

from Norman.messenger.sendAPI import Message
from Norman.settings import MessageConfig
from Norman.utils import response


def get_request_type(payload):
    data = json.loads(payload)
    if "postback" in data["entry"][0]["messaging"][0]:
        return "postback"

    elif "message" in data["entry"][0]["messaging"][0]:
        return "message"


def postback_events(payload):
    data = json.loads(payload)

    postbacks = data["entry"][0]["messaging"]

    for event in postbacks:
        sender_id = event["sender"]["id"]
        postback_payload = event["postback"]["payload"]
        yield sender_id, postback_payload



# if not Mongo.user_exists(users, sender_id):
#     g.user = Mongo.get_user_mongo(users, sender_id)
#     return handle_first_time_user(users, g.user)
#             self.get_started_user_service_list()


messenger = Message()


def handle_get_started(recipient_id):
        user_details = messenger.user_profile.get_user_details(recipient_id)
        message_text = MessageConfig.GET_STARTED_MESSAGE.replace('<username>', user_details['first_name'])
        quick_replies = [
            {"content_type": "text", "title": "What does that mean?", "payload": "NORMAN_GET_STARTED_MEANING"},
            {"content_type": "text", "title": "How do you do that?", "payload": "NORMAN_GET_STARTED_HOW"},
            {"content_type": "text", "title": "What services do you offer", "payload": "NORMAN_GET_SERVICE_LIST"}
                        ]

        messenger.send_message("text", message_text=message_text, recipient_id=recipient_id,  quick_replies=quick_replies)
        return response.response_ok('Success')


def handle_get_started_meaning(recipient_id):
        message_text = MessageConfig.GET_STARTED_MEANING
        quick_replies = [
            {"content_type": "text", "title": "How do you do that?", "payload": "NORMAN_GET_STARTED_HOW"},
            {"content_type": "text", "title": "What services do you offer?", "payload": "NORMAN_GET_ALL_SERVICE_LIST"}
        ]
        messenger.send_message("text", message_text=message_text, recipient_id=recipient_id,  quick_replies=quick_replies)
        return response.response_ok('Success')


def handle_get_started_how(recipient_id):
        message_text = MessageConfig.GET_STARTED_HOW
        quick_replies = [
            {"content_type": "text", "title": "What services do you offer?", "payload": "NORMAN_GET_ALL_SERVICE_LIST"},
            {"content_type": "text", "title": "What are the services am I registered to?",
             "payload": "NORMAN_GET_USER_SERVICE_LIST"}
        ]
        messenger.send_message("text", message_text=message_text, recipient_id=recipient_id, quick_replies=quick_replies)
        return response.response_ok('Success')


def get_started_user_service_list(recipient_id):
        message_text = MessageConfig.GET_STARTED_MEANING
        messenger.send_message("text", message_text=message_text, recipient_id=recipient_id,)


def get_started_service_list(recipient_id):
        message_text = MessageConfig.GET_STARTED_HOW
        quick_replies = [
            {"content_type": "text", "title": "What services do you offer?", "payload": "NORMAN_GET_ALL_SERVICE_LIST"},
            {"content_type": "text", "title": "What are the services am I registered to?",
             "payload": "NORMAN_GET_USER_SERVICE_LIST"}
        ]
        messenger.send_message("text", message_text=message_text, recipient_id=recipient_id,  quick_replies=quick_replies)
        return response.response_ok('Success')


def handle_help(recipient_id):
    message_text = MessageConfig.GET_HELP_MESSAGE
    messenger.send_message("text", message_text=message_text, recipient_id=recipient_id)
    return response.response_ok('Success')