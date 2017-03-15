from flask import Blueprint, jsonify
from flask import json
from flask import make_response
from flask import request
from flask_restful import Resource
from Norman.extensions import csrf_protect
from Norman.utils import response
from Norman.settings import DevConfig
from pymessenger.bot import Bot
from Norman.users.views import UserView
from Norman.facebook.conversations import FreeConversation


bot = Bot(DevConfig.FACEBOOK_SECRET_KEY)
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
        self.user_view = UserView()
        self.free_conversation = FreeConversation()

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
                        return bot.send_text_message(recipient_id, message)
                return make_response(json.dumps({'success': True}), 200,
                                     {'ContentType': 'application/json'})
#                         self.free_conversation.init_conversation()

