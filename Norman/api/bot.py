from flask import Blueprint, jsonify
from flask import make_response
from flask import request
from flask_restful import Resource

from Norman.api.api_ai import AI
from Norman.api.web import UserAPI
from Norman.extensions import csrf_protect
from Norman.messenger.sendAPI import Message
from Norman.norman.user import NormanUser
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
        data = request.get_json()
        for event in data['entry']:
            messaging = event['messaging']
            for action in messaging:
                recipient_id = action['sender']['id']
                self.message = Message(recipient_id)
                if action.get('message'):
                    message_text = action['message']['text']
                    message = ai_response(message_text)
                    m = Message(recipient_id)
                    m.send_message(message_type='text', message_text=message)
                    return response.response_ok('Success')
                else:
                    print(action)
                    self.message.handle_payload(action, recipient_id)
                    return response.response_ok('Success')


def ai_response(message_text):
    ai = AI()  # create AI instance
    ai.parse(message_text)
    if ai.match_successful:
        message = ai.text
    else:
        message = 'Sorry I can\'t handle such requests for now. Services are coming soon'
    return message


@blueprint.route('/test', methods=['POST'])
@csrf_protect.exempt
def test():
    view_class = TestAPI()
    return view_class.post()


class TestAPI(Resource):
    def __init__(self):
        self.user_view = UserAPI()

    def post(self):
        data = request.get_json()
        recipient_id = data['id']
        message = data['message']
        user = NormanUser(recipient_id)
        if user.first_message:
            user.instantiate_user()
            return jsonify({'response': user.start_conversation(message)})
        else:
            user = user.get_user_instance()
            print(user.start_conversation(message, type="existing"))
            return jsonify({'response': user.start_conversation(message, type="existing")})
