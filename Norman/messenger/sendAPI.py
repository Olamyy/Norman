from Norman.api.base import base
from Norman.errors import HttpError
from Norman.settings import FBConfig


graphAPIURL = FBConfig.GRAPH_API_URL.replace('<action>', '/me/messages?')


<<<<<<< HEAD
# class SendAPI:
#     """
#
#     def send_text(self, data):
#         """ Send plain text reply to user
#
#             Usage: Accepts a dictionary of the form
#                 {
#                     'text': 'some text to send',
#                     'recipient': 'valid facebook user id',
#                     'priority': 'a valid priority type' (optional)
#                 }
#
#         """
#
#         if validate_data(data, 'text'):
#             payload = clean_text(data)
#             send_message(payload)
#
#     def send_attachment(self):
#         """ Send attachments to user...
#             Supports: image, audio, video, file
#         """
#         pass
#
#     def send_action(self):
#         """
#             Make chat feel less 'Bot-ty' and more Natural
#             By simulating user actions...
#             Supports: typing_on, typing_off, mark_seen
#         """
#         pass
#
#     def send_button(self):
#         """
#             Request input from the user using buttons.
#             Buttons can:
#             - Open a Specified url
#             - Make a back-end call to specified webhook
#             - Call a phone number
#             - Open a share dialog
#             - open payment dialog
#         """
#         pass
#
#     def send_template(self):
#         """
#             Want to combine multiple response types?
#             No problem, template got you covered ..hehe
#             Supports: image attachment, short description and buttons
#         """
#         pass
#
#
# class Recipient:
#     def __init__(self):
#         self.payload = {'user_id': None}
#
#
# class Message:
#     def __init__(self):
#         self.payload = {
#             "text": None,
#             "attachment": None,
#             "quick_replies": None,
#             "metadata": None
#         }
#
#
# class Payload:
#     def __init__(self, recipient, message=None, sender_action=None, notification_type="REGULAR"):
#         self.payload = {
#             "recipient": recipient,
#             "message": message,
#             "sender_action": sender_action,
#             "notification_type": notification_type
#         }
#
#
# def validate_data(data, response_type):
#
#         text = data.get('text', None)
#         recipient_id = data.get('recipient_id', None)
#
#         if response_type is 'text':
#             if text and recipient_id:
#                 return True
#
#
# class Button:
#     """ Feature:
#         - type: web_url or postback
#         - title: text displayed on the screen
#         - url: only valid for type web_url
#         - payload: only valid for type postback
#
#     """
#
#     def __init__(self):
#         self.content = {
#             "type": None,
#             "url": None,
#             "title": None,
#             "payload": None
#           }
#
#
# class TemplateList:
#     pass
#
#
# class list_item:
#     def __init__(self):
#         self.content = {
#
#             "title": None,
#             "image_url": None,
#             "subtitle": None,
#             "default_action": {
#                 "type": "web_url",
#                 "url": "https://peterssendreceiveapp.ngrok.io/shop_collection",
#                 "messenger_extensions": True,
#                 "webview_height_ratio": "tall",
#                 "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
#                 },
#             "buttons": [
#                 {
#                     "title": "Shop Now",
#                     "type": "web_url",
#                     "url": "https://peterssendreceiveapp.ngrok.io/shop?item=100",
#                     "messenger_extensions": True,
#                     "webview_height_ratio": "tall",
#                     "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
#                 }
#             ]
#                 }
#
#
# def clean_message(data):
#     """Accepts a dictionary"""
#     pass
#
#
# def clean_text(data):
#     text = data.get('text', None)
#     recipient_id = data.get('recipient_id', None)
#
#     recipient_obj = Recipient()
#     message_obj = Message()
#
#     recipient_obj.payload['user_id'] = recipient_id
#     message_obj.payload['text'] = text
#
#     message_payload = clean_payload(message_obj.payload)
#     recipient_payload = clean_payload(recipient_obj.payload)
#
#     final_payload = Payload(message_payload, recipient_payload)
#     return clean_payload(final_payload.payload)
#
#
# def send_message(payload):
#     # request = base.exec_request('POST', graphAPIURL, data=payload)
#     # if request:
#     #     print(request)
#     # else:
#     #     raise HttpError('Unable to complete request.')
#     print(payload)
#
#
# def clean_payload(payload):
#     new_payload = payload.copy()
#     for entry in payload:
#         if not payload[entry]:
#             new_payload.pop(entry)
#     return new_payload

=======
>>>>>>> 1b4045a213ba7c4ff3d13d20e790ab3f221d2a77
class Message(object):

    def __init__(self, recipient_id, **kwargs):
        self.recipient_id = recipient_id
        self.notification_type = None
        self.payload_structure = {
                                  'recipient_id': self.recipient_id,
                                  'message': {
                                      "text": '',
                                      'attachment': {
                                          'type': '',
                                          'payload': {
                                              'template_type': '',
                                              'url': '',
                                              'title': ''
                                          },
                                      }
                                  },
                                  'sender_action': '',
                                  'notification_type': ''
                                }

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

    def send_message(self, message_type, message_text=None, attachment=None, notification_type=None):
        """
        - text must be UTF-8 and has a 640 character limit
        - You cannot send a text and an attachment together
        :param message_type: text or attachment
        :param message_text: text to send
        :param attachment: a valid attachment object i.e dictionary
        :param notification_type: REGULAR, SILENT_PUSH, or NO_PUSH
        :return: json response object
        """
        notification_type = notification_type

        if message_type == "text":
            self.payload_structure['message']['text'] = message_text
            self.payload_structure['message'].pop('attachment')
        else:
            self.payload_structure['message'].pop('text')
            self.payload_structure['message']['attachment'] = attachment

        # clean up payload
        self.payload_structure.pop('sender_action')
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
            self.payload_structure['message']['buttons'] = [kwargs.get('buttons')]
        else:
            self.payload_structure.pop('buttons')
