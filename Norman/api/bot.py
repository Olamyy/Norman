from flask import Blueprint, jsonify
from flask import make_response
from flask import request
from flask_restful import Resource
from Norman.api.web import UserAPI
from Norman.extensions import csrf_protect
from Norman.messenger.Utils import get_request_type, postback_events, messaging_events
from Norman.messenger.sendAPI import PostBackMessages
from Norman.utils import response


blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/', methods=['GET', 'POST'])
@csrf_protect.exempt
def helloworld():
    view_class = HelloWorld()
    if request.method == "GET":
        return view_class.get()
    else:
        return view_class.post()


class HelloWorld(Resource):
    def get(self):
        return jsonify({'hello': 'world'})

    def post(self):
        return jsonify({'method': 'POST'})


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
                print("I got a postback")
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
                # norman = NormanUser(recipient_id)
                # messenger = Message(recipient_id)
                # message_response = NLPProcessor(message, recipient_id)
                # norman = NormanUser(recipient_id)
                # context = norman.getuserContext()
                # messenger = Message(recipient_id)
                # decipher_message = norman.process_message(message, recipient_id)
                # noun_phrase = decipher_message.findNounPhrase()
                # if decipher_message.isAskingBotInfo():
                #     return messenger.handleBotInfo()
                # if context is not None and len(context) > 0:
                #     context = context[-1]
                #
                #     if decipher_message.isDismissPreviousRequest():
                #         return norman.popContexts(context)
                #
                #     if context == 'find-food':
                #         return messenger.handle_find_food(context, message, noun_phrase, message,
                #                                           'receive_location_text')
                #
                #     elif context['context'] == 'yelp-rename':
                #         messenger.handle_yelp_rename(context, message)
                #         return norman.popContexts(context)  # pop yelp-rename
                #
                #     elif context['context'] == 'create-reminder':
                #         return messenger.initService('create-reminder')
                # if message['type'] == "location":
                #     return messenger.handleLocation()
                # else:
                #     if decipher_message.isGreetings():
                #         return messenger.handleGreeting(decipher_message.sayHiTimeZone(recipient_id))
                #
                #     elif decipher_message.isGoodbye():
                #         return messenger.handleGoodbye(decipher_message.sayByeTimeZone())
                #
                #     elif decipher_message.isYelp():
                #         return messenger.handleYelp(None, noun_phrase, message, 'receive_request')
                #
                #     else:
                #         # Log this message for categorization later
                #         norman.handleUncategorized("text", message)
                #         ##@Todo: Handle APIAI Responses here
                print(data)
                postbackmessages = PostBackMessages(recipient_id)
                return postbackmessages.handle_api_ai_message(message)

        else:
            return response.response_ok('success')
