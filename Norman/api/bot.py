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
    else:
        return view_class.post()


class WebHook(Resource):
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
            for x in messaging:
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    if x['message'].get('text'):
                        message = x['message']['text']
        print(data)
        if data.get('object', None) == 'page':
            message_entries = data['entry']
            for entry in message_entries:
                # page_id = entry['id']
                # time_of_event = entry['time']
                for event in entry['messaging']:
                    if event.get('message', None):
                        make_response(json.dumps({'success': True}), 200,
                                      {'ContentType': 'application/json'})
                        self.reply(event)

    def reply(self, event):
        sender_id = event['sender']['id']
        # recipient_id = event['recipient']['id']
        # time_of_message = event['timestamp']
        message = event['message']

        # message_id = message['mid']
        message_text = message.get('text', None)
        message_attachments = message.get('attachments', None)

        if message_text:
            if message_text == 'generic':
                self.send_generic_message(sender_id)
            else:
                self.send_text_message(sender_id, message_text)
        elif message_attachments:
            print("message with attachment received")
            self.send_text_message(sender_id)

    def send_generic_message(self, recipient_id):
        generic_greeting = "Hello, I'm Norman, your personal assistant\
          I help you keep track of your health."
        message_data_dict = {'recipient': {'id': recipient_id}, 'message': {'text': generic_greeting}}
        message_data = json.dumps(message_data_dict)
        self.call_send_api(message_data)

    def send_text_message(self, recipient_id, message_text=None):
        message_data = {'recipient': {'id': recipient_id}, 'message': {'text': message_text}}
        print('message_data: ', message_data)
        self.call_send_api(message_data)

    @staticmethod
    def call_send_api(message):
        # access_token = 'EAAS0PtgoBk4BAKIZBKELBTB7JZBsoetjvG1A3xmMWhJFlDxeUtfgNgr2odxHZBqZAailae0ev0PaIzLz7ifaWEAfIKTfWGy35yjejmzA9OJVhH2mxMPNGXzBhE397hWZBJhP8Uz0uJ588lJ4jW5DQN0544Gq1d7BuqYBAxflaiQZDZD'
        uri = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAS0PtgoBk4BAOOxYN9iU0LbCMs3ZAxNDuTsObMSu6VrENInETL7TrZCZCGGjOvcWgM7zAUNsHaAtr7AwJgWpZB68aUGIBlZCzau2ZCFmTUBI5MqP8xJaejv9uMwKdKhNYgGWPJXGfd8OvGZBulzwRBG8sGQdJfGAlKLsfigkBxkgZDZD'
        try:
            resp = r.post(uri, json=message)
            print(resp.status_code)
            print(resp.text)
        except r.ConnectionError:
            print('Unable to connect to graph api')


@blueprint.route('/test-mongo', methods=['POST'])
@csrf_protect.exempt
def test_mongo():
    name = request.args.get('name')
    init_db = Todo.objects.all()
    print(init_db)
    return name
