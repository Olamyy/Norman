from flask import Blueprint, jsonify
from flask import make_response
from flask import request
from flask_restful import Resource
from Norman.extensions import csrf_protect
from Norman.utils import response
from Norman.settings import DevConfig
from Norman.hospital.models import Todo
from pymessenger.bot import Bot

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


class WebHook(Resource):
    def get(self):
        args = request.args
        verify_token = 'python_rocks'
        if args.get('hub.mode') == 'subscribe' and args.get('hub.verify_token') == verify_token:
            return make_response(args.get('hub.challenge').strip("\n\""))
        else:
            return response.response_error('Failed validation. Make sure the validation tokens match', args)
    
    def post(self):
        output = request.get_json()
        print("The output is ", output)
        for event in output['entry']:
            print("The event is", event)
            messaging = event['messaging']
            print("The message event is,", messaging)
            for x in messaging:
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    print("The recipient ID is", recipient_id)
                    if x['message'].get('text'):
                        message = x['message']['text']
                        print("The message is", message)
                        bot.send_text_message(recipient_id, message)
                    if x['message'].get('attachments'):
                        for att in x['message'].get('attachments'):
                            print("att is", att)
                            bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])
                else:
                    print("WTF")
                    return "ok"
        return "Success"


@blueprint.route('/test-mongo', methods=['POST'])
@csrf_protect.exempt
def test_mongo():
    name = request.args.get('name')
    init_db = Todo.objects.all()
    print(init_db)
    return name
