from flask import Blueprint, jsonify
from flask import make_response
from flask import request
from flask_restful import Resource

from Norman.api.api_ai import AI
from Norman.api.web import UserAPI
from Norman.extensions import csrf_protect
from Norman.messenger.Utils import get_request_type, postback_events, handle_help, handle_get_started, \
    handle_get_started_meaning, handle_get_started_how, get_started_user_service_list, get_started_service_list
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
                if postback_payload == 'NORMAN_GET_HELP':
                    handle_help(recipient_id)
                elif postback_payload == 'NORMAN_GET_STARTED_PAYLOAD':
                    handle_get_started(recipient_id)
                elif postback_payload == 'NORMAN_GET_STARTED_MEANING':
                    handle_get_started_meaning(recipient_id)
                elif postback_payload == 'NORMAN_GET_STARTED_HOW':
                    handle_get_started_how(recipient_id)
                elif postback_payload == 'NORMAN_GET_USER_SERVICE_LIST':
                    get_started_user_service_list(recipient_id)
                elif postback_payload == 'NORMAN_GET_SERVICE_LIST':
                    get_started_service_list(recipient_id)

        elif request_type == "message":
            pass
        return response.response_ok('Success')
        # for event in data['entry']:
        #     print(event)
        #     messaging = event['messaging']
        #     print(messaging)
        #     for action in messaging:
        #         print(action)
        #         recipient_id = action['sender']['id']
        #         self.message = Message(recipient_id)
        #         if action.get('message'):
        #             self.message.send_message(message_type='text', message_text='Hello')
        #             return response.response_ok('Success')
        #         else:
        #             self.message.handle_payload(action, recipient_id)
        #             return response.response_ok('Success')
        #     return response.response_ok('Success')


def ai_response(message_text):
    ai = AI()  # create AI instance
    ai.parse(message_text)
    if ai.match_successful:
        message = ai.text
    else:
        message = 'Sorry I can\'t handle such requests for now. Services are coming soon'
    return message

