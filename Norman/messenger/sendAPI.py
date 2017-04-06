from Norman.api.base import base
from Norman.errors import HttpError
from Norman.settings import FBConfig

# Buttons
# Quick Replies
# Sender Actions
# Upload API
# Error Codes

graphAPIURL = FBConfig.GRAPH_API_URL.replace('<action>', '/me/messages?')


class Message(object):
    def __init__(self, recipient_id, **kwargs):
        self.recipient_id = recipient_id
        self.notification_type = None
        self.payload_structure = {
                                  'recipient_id': self.recipient_id,
                                  'message': {
                                      "text": ''
                                  },
                                  'user_action': {
                                      'user_action': ''
                                  },
                                  'attachment': {
                                      'type': '',
                                      'payload': {
                                          'template_type': '',
                                          'url': '',
                                          'title': ''
                                      },

                                  },
                                    }

    def send_action(self, action):
        """

        :return:
        """
        self.payload_structure.pop('attachment')
        self.payload_structure['user_action']['user_action'] = action
        request = base.exec_request('POST', graphAPIURL, data=self.payload_structure)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')

    def send_message(self, message_type, message, attachment_url=None):
        """

        :return:
        """
        attachment_url = attachment_url
        self.payload_structure.pop('user_action')
        if message_type == "text":
            self.payload_structure['message']['text'] = message
            self.payload_structure.pop('attachment')
        else:
            self.payload_structure['attachment'] = {'type': message_type}
            self.payload_structure['attachment']['payload'] = {'url': attachment_url}
        request = base.exec_request('POST', graphAPIURL, data=self.payload_structure)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')


class Template(Message):
    def __init__(self, recipient_id, **kwargs):
        super().__init__(recipient_id, **kwargs)
        self.payload_structure["attachment"]["type"] = "template"
        self.payload_structure["attachment"]["payload"]["template_type"] = ""
        self.payload_structure["attachment"]["payload"]["buttons"] = {}
        self.payload_structure["attachment"]["payload"]["elements"] = {
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

                                             }

    def send_template_message(self, template_type, **kwargs):
        if template_type == "button":
            self.payload_structure["attachment"]["payload"]["text"] = kwargs.get('text')
            self.payload_structure['attachment']['payload'].pop('elements')
            self.payload_structure["attachment"]["payload"]["template_type"] = template_type
            self.payload_structure['buttons'] = [kwargs.get('buttons')]
        else:
            pass



