from flask import Blueprint, jsonify
from flask import make_response
from flask import request
from flask_restful import Resource
from pymessenger.bot import Bot

from Norman.api.web import UserAPI
from Norman.extensions import csrf_protect
from Norman.norman.user import NormanUser
from Norman.settings import FBConfig
from Norman.utils import response

bot = Bot(FBConfig.FACEBOOK_SECRET_KEY)
blueprint = Blueprint('api', __name__ , url_prefix='/api')


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
                if action.get('message'):
                    recipient_id = action['sender']['id']
                    if not self.user_view.validate_user(recipient_id):
                        message = "Hello, {0}".format(recipient_id)
                        user = NormanUser(recipient_id)
                        if user.first_message:
                            user.instantiate_user()
                            bot.send_text_message(recipient_id, user.start_conversation(message, type="new"))
                            return response.response_ok('Success')
                        else:
                            user = user.get_user_instance()
                            bot.send_text_message(recipient_id, user.start_conversation(message, type="new"))
                            return response.response_ok('Success')


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
            return jsonify({'response': user.start_conversation(message, type="new")})
        else:
            user = user.get_user_instance()
            return jsonify({'response': user.start_conversation(message, type="existing")})



