from Norman.api.base import base
from Norman.errors import HttpError
from Norman.messenger.userProfile import Profile
from Norman.norman.user import UserUtils
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
        # self.payload_structure.pop('message')
        self.payload_structure.pop('notification_type')
        self.payload_structure['sender_action'] = action

        # connect
        request = base.exec_request('POST', graphAPIURL, data=self.payload_structure)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')

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
        request = base.exec_request('POST', graphAPIURL, data=self.payload_structure)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')


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
            try:
                self.payload_structure.pop('buttons')
            except KeyError:
                pass

        # clean up payload
        self.payload_structure.pop('sender_action')
        notification_type = kwargs.get('notification_type')
        if notification_type:
            self.payload_structure['notification_type'] = notification_type
        else:
            self.payload_structure.pop('notification_type')
        quick_replies = kwargs.get('notification_type')
        if quick_replies:
            self.payload_structure['quick_replies'] = quick_replies
        else:
            self.payload_structure['message'].pop('quick_replies')
        self.payload_structure['message'].pop('text')
        request = base.exec_request('POST', graphAPIURL, data=self.payload_structure)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')


class PostBackMessages(Message):
    def __init__(self, recipient_id, **kwargs):
        super().__init__(recipient_id, **kwargs)
        self.current_user = UserUtils(recipient_id)

    def handle_get_started(self, recipient_id):
        template = Template(recipient_id)
        if self.current_user.is_first_message():
            self.current_user.update_first_message()
        user_details = self.user_profile.get_user_details(recipient_id)
        message_text = MessageConfig.GET_STARTED_MESSAGE.replace('<username>', user_details['first_name'])
        norman_get_started_meaning = {
            "title": "Quick Help",
            "image_url": "https://ca858b96.ngrok.io/static/landing/images/",
            "subtitle": "View a list of FAQs on our site",
            "default_action": {
                "type": "web_url",
                "url": "https://ca858b96.ngrok.io#faqs-section",
                "messenger_extensions": True,
                "webview_height_ratio": "tall",
                "fallback_url": "https://ca858b96.ngrok.io/"
            },
            "buttons": [
                {
                    "title": "Shop Now",
                    "type": "web_url",
                    "url": "https://peterssendreceiveapp.ngrok.io/shop?item=100",
                    "messenger_extensions": True,
                    "webview_height_ratio": "tall",
                    "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                }
            ]
        }
        self.send_message("text", message_text=message_text)
        template.send_template_message(template_type='list', list_info=[norman_get_started_meaning])
        return response.response_ok('Success')

    def handle_get_started_meaning(self):
        message_text = MessageConfig.GET_STARTED_MEANING
        quick_replies = [
            {"content_type": "text", "title": "How do you do that?", "payload": "NORMAN_GET_STARTED_HOW"},
            {"content_type": "text", "title": "What services do you offer?", "payload": "NORMAN_GET_ALL_SERVICE_LIST"}
        ]
        self.send_message("text", message_text=message_text, quick_replies=quick_replies)
        return response.response_ok('Success')

    def handle_get_started_how(self):
        print("I got to handle_get_started_how ")
        message_text = MessageConfig.GET_STARTED_HOW
        quick_replies = [
            {"content_type": "text", "title": "What services do you offer?", "payload": "NORMAN_GET_ALL_SERVICE_LIST"},
            {"content_type": "text", "title": "What are the services am I registered to?",
             "payload": "NORMAN_GET_USER_SERVICE_LIST"}
        ]
        self.send_message("text", message_text=message_text,
                               quick_replies=quick_replies)
        return response.response_ok('Success')

    def get_started_user_service_list(self):
        print("I got to get_started_user_service_list ")
        message_text = MessageConfig.GET_STARTED_MEANING
        self.send_message("text", message_text=message_text, )

    def get_started_service_list(self):
        print("I got to get_started_service_list")
        message_text = MessageConfig.GET_STARTED_HOW
        quick_replies = [
            {"content_type": "text", "title": "What services do you offer?", "payload": "NORMAN_GET_ALL_SERVICE_LIST"},
            {"content_type": "text", "title": "What are the services am I registered to?",
             "payload": "NORMAN_GET_USER_SERVICE_LIST"}
        ]
        self.send_message("text", message_text=message_text,
                               quick_replies=quick_replies)
        return response.response_ok('Success')

    def handle_help(self):
        print("I got to handle help")
        message_text = MessageConfig.GET_HELP_MESSAGE
        self.send_message("text", message_text=message_text)
        return response.response_ok('Success')