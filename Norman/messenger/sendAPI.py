from Norman.api.base import base
from Norman.errors import HttpError
from Norman.messenger.userProfile import Profile
from Norman.settings import FBConfig, MessageConfig
from Norman.utils import response

graphAPIURL = FBConfig.GRAPH_API_URL.replace('<action>', '/me/messages?')


class Message(object):
    def __init__(self, recipient_id, **kwargs):
        self.recipient_id = recipient_id
        self.notification_type = None
        self.payload_structure = {
                                  'recipient': {
                                                'id': self.recipient_id
                                                },
                                  'message': {
                                      'text': '',
                                      'attachment': {
                                          'type': '',
                                          'payload': {
                                              'template_type': '',
                                              'text': '',
                                              'buttons': ''
                                          },
                                      },
                                      'quick_replies': []
                                  },
                                  'sender_action': '',
                                  'notification_type': ''
                                }
        self.user_profile = Profile()

    def send_action(self, action):
        """
        :param action: - typing_on, typing_off, mark_as_read
        """
        # clean up payload
        self.payload_structure.pop('message')
        self.payload_structure.pop('notification_type')
        self.payload_structure['sender_action'] = action

        # connect
        request = base.exec_request('POST', graphAPIURL, data=self.payload_structure)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')

    def is_get_started(self, action):
            pass

    def send_message(self, message_type, message_text=None, attachment=None, notification_type=None, quick_replies=None):
        """
        - text must be UTF-8 and has a 640 character limit
        - You cannot send a text and an attachment together
        :param quick_replies: a list of quick responses sent along with the message to the user
        :param message_type: text or attachment
        :param message_text: text to send
        :param attachment: a valid attachment object i.e dictionary
        :param notification_type: REGULAR, SILENT_PUSH, or NO_PUSH
        :return: json response object
        """
        notification_type = notification_type
        quick_replies = quick_replies

        if message_type == "text":
            self.payload_structure['message']['text'] = message_text
            self.payload_structure['message'].pop('attachment')
        else:
            self.payload_structure['message'].pop('text')
            self.payload_structure['message']['attachment'] = attachment

        # clean up payload
        self.payload_structure.pop('sender_action')
        if quick_replies:
            self.payload_structure['message']['quick_replies'] = quick_replies
        else:
            self.payload_structure['message'].pop('quick_replies')
        if notification_type:
            self.payload_structure['notification_type'] = notification_type
        else:
            self.payload_structure.pop('notification_type')

        # connect
        print(self.payload_structure)
        request = base.exec_request('POST', graphAPIURL, data=self.payload_structure)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')

    def handle_payload(self, action, recipient_id):
        postback = action.get('postback')
        print('The postback is', postback)
        payload = postback['payload']
        print("The payload is", payload)
        if payload == 'GET_STARTED_PAYLOAD':
            self.handle_get_started(recipient_id)
        elif payload == 'GET_STARTED_MEANING':
            self.handle_get_started_meaning()
        elif payload == 'GET_STARTED_HOW':
            self.handle_get_started_how()
        elif payload == 'GET_ALL_SERVICE_LIST':
            self.get_started_service_list()
        else:
            self.get_started_user_service_list(recipient_id)

    def handle_get_started(self, recipient_id):
        user_details = self.user_profile.get_user_details(recipient_id)
        message_text = MessageConfig.GET_STARTED_MESSAGE.replace('<username>', user_details['first_name'])
        quick_replies = [
            {"content_type": "text", "title": "What does that mean?", "payload": "GET_STARTED_MEANING"},
            {"content_type": "text", "title": "How do you do that?", "payload": "GET_STARTED_HOW"},
            {"content_type": "text", "title": "What services do you offer", "payload": "GET_SERVICE_LIST"}
        ]

        self.send_message("text", message_text=message_text, quick_replies=quick_replies)
        return response.response_ok('Success')

    def handle_get_started_meaning(self,):
        message_text = MessageConfig.GET_STARTED_MEANING
        quick_replies = [
            {"content_type": "text", "title": "How do you do that?", "payload": "GET_STARTED_HOW"},
            {"content_type": "text", "title": "What services do you offer?", "payload": "GET_SERVICE_LIST"}
        ]
        self.send_message("text", message_text=message_text, quick_replies=quick_replies)
        return response.response_ok('Success')

    def handle_get_started_how(self):
        message_text = MessageConfig.GET_STARTED_HOW
        quick_replies = [
            {"content_type": "text", "title": "What services do you offer?", "payload": "GET_ALL_SERVICE_LIST"},
            {"content_type": "text", "title": "What are the services am I registered to?",
             "payload": "GET_USER_SERVICE_LIST"}
        ]
        self.send_message("text", message_text=message_text, quick_replies=quick_replies)
        return response.response_ok('Success')

    def get_started_user_service_list(self, recipient_id):
        pass

    def get_started_service_list(self):
        message_text = MessageConfig.GET_STARTED_HOW
        quick_replies = [
            {"content_type": "text", "title": "What services do you offer?", "payload": "GET_ALL_SERVICE_LIST"},
            {"content_type": "text", "title": "What are the services am I registered to?",
             "payload": "GET_USER_SERVICE_LIST"}
        ]
        self.send_message("text", message_text=message_text, quick_replies=quick_replies)
        return response.response_ok('Success')


class Template(Message):
    def __init__(self, recipient_id, **kwargs):
        super().__init__(recipient_id, **kwargs)
        self.payload_structure['message']["attachment"]["type"] = "template"
        self.payload_structure['message']["attachment"]["payload"]["buttons"] = {}
        self.payload_structure['message']["attachment"]["payload"]["elements"] = [{
                                             'title': "",
                                             'image_url': "",
                                             'subtitle': "",
                                             'default_action': {
                                                 'type': '',
                                                 'url': '',
                                                 'messenger_extensions': '',
                                                 'webview_height_ratio': '',
                                                 'fallback_url': ''
                                             },
                                             'buttons': {
                                                         'title': '',
                                                         'type': '',
                                                         'url': '',
                                                         'messenger_extensions': '',
                                                         'webview_height_ratio': '',
                                                         'fallback_url': ''
                                                         }

                                             }]

    def send_template_message(self, template_type, **kwargs):
        self.payload_structure["message"]["attachment"]["payload"]["template_type"] = template_type

        if template_type == "button":
            self.payload_structure['message']["attachment"]["payload"]["text"] = kwargs.get('text')
            self.payload_structure['message']['attachment']['payload'].pop('elements')
        elif template_type == 'generic':
            self.payload_structure['message']["attachment"]["payload"]['elements'][0] = kwargs.get('generic_info')
        elif template_type == 'list':
            self.payload_structure['message']["attachment"]["payload"]['elements'][0] = kwargs.get('list_info')

        if kwargs.get("buttons"):
            self.payload_structure['message']["attachment"]["payload"]['buttons'] = [kwargs.get('buttons')]
        else:
            self.payload_structure.pop('buttons')

        # clean up payload
        self.payload_structure.pop('sender_action')
        notification_type = kwargs.get('notification_type')
        if notification_type:
            self.payload_structure['notification_type'] = notification_type
        else:
            self.payload_structure.pop('notification_type')
        request = base.exec_request('POST', graphAPIURL, data=self.payload_structure)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')