from flask import Flask, request, make_response
from flask_restful import Resource, Api
import os
import json
import requests as r

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    @staticmethod
    def get():
        return json.dumps({'hello': 'world'})


class WebHook(Resource):
    @staticmethod
    def get():
        args = request.args
        verify_token = 'python_rocks'
        if args.get('hub.mode') == 'subscribe' and args.get('hub.verify_token') == verify_token:
            print('validating webhook')
            return make_response(args.get('hub.challenge').strip("\n\""))
        else:
            print('Failed validation. Make sure the validation tokens match')

    def post(self):
        data = request.get_json()
        print(data)
        if data.get('object', None) == 'page':
            message_entries = data['entry']
            for entry in message_entries:
                # page_id = entry['id']
                # time_of_event = entry['time']
                for event in entry['messaging']:
                    if event.get('message', None):
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
        message_data_dict = {'recipient': {'id': recipient_id}, 'message': {'text': message_text}}
        message_data = json.dumps(message_data_dict)
        self.call_send_api(message_data)

    @staticmethod
    def call_send_api(message):
        access_token = 'EAAS0PtgoBk4BAAV6pDrocKGlPOAjdxyn' \
                       'xBidP5noah1l27yRu2x0zZAc' \
                       '1clvjQN1YAY9dHgJKGd8fPqjwHB' \
                       'xQ0KuQxUahCkxUDmecH9OQvAk8FK' \
                       'uZBZA2jQhHPihh85WcALD8UZBMRx' \
                       'YXT1iAqaAGdpUcjKAlOBwL6VwisVC8QZDZD'
        uri = 'https://graph.facebook.com/v2.6/me/messages/access_token=' + access_token
        try:
            resp = r.post(uri, json=message)
            print(resp.status_code, '\n')
            print(resp.text)
        except r.ConnectionError:
            print('Unable to connect to graph api')


api.add_resource(HelloWorld, '/')
api.add_resource(WebHook, '/webhook')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
