from flask import Blueprint, jsonify
from flask import make_response
from flask import request
from flask_restful import Resource
from Norman.api.web import UserAPI
from Norman.extensions import csrf_protect
from Norman.messenger.Utils import get_request_type, postback_events, messaging_events
from Norman.messenger.sendAPI import PostBackMessages, Message
from Norman.norman.processor import Processor
from Norman.norman.user import NormanUser
from Norman.messenger.sendAPI import PostBackMessages
from Norman.utils import response


blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/webhook', methods=['GET', 'POST'])
@csrf_protect.exempt
def webhook():
    view_class = WebHook()
    if request.method == "GET":
        return view_class.get()
    else:
        return view_class.post()


class WebHook(Resource):
    def __init__(self):
        self.user_view = UserAPI()
        self.message = None

    @staticmethod
    def get():
        args = request.args
        verify_token = 'python_rocks'
        if args.get('hub.mode') == 'subscribe' and args.get('hub.verify_token') == verify_token:
            return make_response(args.get('hub.challenge').strip("\n\""))
        else:
            return response.response_error('Failed validation. Make sure the validation tokens match', args)

    def post(self):
        data = request.get_data()
        request_type = get_request_type(data)

        if request_type == 'postback':
            for recipient_id, postback_payload in postback_events(data):
                postbackmessages = PostBackMessages(recipient_id)
                print(postback_payload)
                if postback_payload == 'NORMAN_GET_HELP':
                    return postbackmessages.handle_help()
                elif postback_payload == 'NORMAN_GET_STARTED_PAYLOAD':
                    return postbackmessages.handle_get_started()
                elif postback_payload == 'NORMAN_GET_STARTED_MEANING':
                    return postbackmessages.handle_get_started_meaning()
                elif postback_payload == 'NORMAN_GET_STARTED_HOW':
                    return postbackmessages.handle_get_started_how()
                elif postback_payload == 'NORMAN_GET_ALL_SERVICE_LIST':
                    return postbackmessages.get_started_service_list()
                elif postback_payload == 'GOOD_TO_GO':
                    return postbackmessages.good_to_go()
                elif postback_payload == 'NORMAN_LEAVE_MESSAGE':
                    return postbackmessages.handle_leave_message()
                elif postback_payload == 'NORMAN_SET_REMINDER':
                    return postbackmessages.handle_set_reminder()
                elif postback_payload == 'NORMAN_REQUEST_URGENT_HELP':
                    return postbackmessages.handle_request_urgent_help()
                elif postback_payload == 'NORMAN_BOOK_APPOINTMENT':
                    return postbackmessages.handle_book_appointment()
                elif postback_payload == 'GET_NEARBY_HOSPITAL':
                    return postbackmessages.handle_get_nearby_hospital()
                elif postback_payload == 'GOOD_TO_GO_FREE':
                    return postbackmessages.good_to_go_free()
                return response.response_ok('success')

        elif request_type == "message":
            for recipient_id, message in messaging_events(data):
                if not message:
                    return response.response_ok('Success')
                message = Message(recipient_id)
                message_response = Processor(message, recipient_id)
                message.send_message(message_response)
                ###@Todo: Handle APIAI Responses here
                # postbackmessages = PostBackMessages(recipient_id)
                # message_text = message['data'].decode('unicode_escape')
                # return postbackmessages.handle_api_ai_message(message_text)

        else:
            return response.response_ok('success')
        data = request.get_json()
        for event in data['entry']:
            messaging = event['messaging']
            for action in messaging:
                if action.get('message'):
                    recipient_id = action['sender']['id']
                    bot = Message(recipient_id)
                    if not self.user_view.validate_user(recipient_id):
                        message = "Hello {0}, I'm Norman. Type Help to get started".format(recipient_id)
                        bot.send_message(recipient_id, message)
                        return response.response_ok('success')
#                         self.free_conversation.init_conversation()
