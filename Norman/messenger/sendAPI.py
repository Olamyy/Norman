import requests
from flask import json
from Norman import settings
from Norman.api.base import base
from Norman.errors import HttpError
from Norman.messenger.userProfile import Profile
from Norman.norman.user import NormanUser, TempUser, MessagingService
from Norman.settings import FBConfig, MessageConfig, ServiceListConfig
from Norman.utils import response
from Norman.api.api_ai import AI

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

    @staticmethod
    def show_typing(recipient_id, action='typing_on'):
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                          params={"access_token": settings.FBConfig.FACEBOOK_SECRET_KEY},
                          data=json.dumps({
                              "recipient": {"id": recipient_id},
                              "sender_action": action
                          }),
                          headers={'Content-type': 'application/json'})
        if r.status_code != requests.codes.ok:
            return response.response_ok('Success')

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
            try:
                self.payload_structure['message'].pop('attachment')
            except KeyError:
                pass
        else:
            try:
                self.payload_structure['message'].pop('text')
            except KeyError:
                pass
            self.payload_structure['message']['attachment'] = attachment

        # clean up payload
        try:
            self.payload_structure.pop('sender_action')
        except KeyError:
            pass
        if quick_replies:
            self.payload_structure['message']['quick_replies'] = quick_replies
        else:
            try:
                self.payload_structure['message'].pop('quick_replies')
            except KeyError:
                pass
        if notification_type:
            self.payload_structure['notification_type'] = notification_type
        else:
            try:
                self.payload_structure.pop('notification_type')
            except KeyError:
                pass

        # connect
        request = base.exec_request('POST', graphAPIURL, data=self.payload_structure)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')

    def handleGreeting(self, timeContext):
        pass

    def handleBotInfo(self):
        pass

    def handle_find_food(self, context, message, noun_phrase, message1, param):
        pass

    def handle_yelp_rename(self, context, message):
        pass

    def handle_memo(self, message_text):
        pass

    def initService(self, param):
        pass

    def handleGoodbye(self, param):
        pass

    def handleYelp(self, param, noun_phrase, message, param1):
        pass

    def handleLocation(self):
        pass


class Template(Message):
    def __init__(self, recipient_id, **kwargs):
        super(Template, self).__init__(recipient_id, **kwargs)
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
            self.payload_structure['message']["attachment"]["payload"]['elements'] = kwargs.get('list_info')
            self.payload_structure['message']['attachment']['payload'].pop('text')
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
        print(self.payload_structure)
        request = base.exec_request('POST', graphAPIURL, data=self.payload_structure)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')


class PostBackMessages(Template):
    def __init__(self, recipient_id, **kwargs):
        super(PostBackMessages, self).__init__(recipient_id, **kwargs)
        self.recipient_id = recipient_id
        self.temp_user = None
        self.current_user = NormanUser(recipient_id)
        self.user_details = self.user_profile.get_user_details(recipient_id)

    def handle_get_started(self):
        self.temp_user = TempUser(self.recipient_id)
        message_text = MessageConfig.GET_STARTED_MESSAGE.replace('<username>', self.user_details['first_name'])
        quick_replies = [
            {"content_type": "text", "title": "What does that mean?", "payload": "NORMAN_GET_STARTED_MEANING"},
            {"content_type": "text", "title": "How do you do that?", "payload": "NORMAN_GET_STARTED_HOW"},
        ]
        self.send_message("text", message_text=message_text, quick_replies=quick_replies)
        response.response_ok('Success')
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
        # self.current_user.
        message_text = MessageConfig.GET_STARTED_HOW
        quick_replies = [
            {"content_type": "text", "title": "What services do you offer?", "payload": "NORMAN_GET_ALL_SERVICE_LIST"},
            {"content_type": "text", "title": "Nice", "payload": "GOOD_TO_GO"},
            {"content_type": "text", "title": "I'm still confused",
             "payload": "NORMAN_GET_HELP"}
        ]
        self.send_message("text", message_text=message_text, quick_replies=quick_replies)
        return response.response_ok('Success')

    def get_started_service_list(self):
        # self.send_message("text", message_text="Here are the services we offer")
        self.send_template_message(template_type='list', list_info=[ServiceListConfig.messaging,
                                                                    ServiceListConfig.reminder,
                                                                    ServiceListConfig.emergency,
                                                                    ServiceListConfig.scheduling
                                                                    ])
        message_text = MessageConfig.GET_ALL_SERVICE_LIST.replace('<username>', self.user_details['first_name'])
        quick_replies = [
            {"content_type": "text", "title": "Nice", "payload": "GOOD_TO_GO"},
            {"content_type": "text", "title": "I'm still confused",
             "payload": "NORMAN_GET_HELP"}
        ]
        self.send_message("text", message_text=message_text, quick_replies=quick_replies)
        return response.response_ok('Success')

    def handle_help(self):
        message_text = MessageConfig.GET_HELP_MESSAGE.replace('<username>', self.user_details['first_name'])
        quick_replies = [
            {"content_type": "text", "title": "Tell Me About You", "payload": "NORMAN_GET_STARTED_PAYLOAD"},
            {"content_type": "text", "title": "Leave a Message", "payload": "NORMAN_LEAVE_MESSAGE"},
            {"content_type": "text", "title": "Set Reminder", "payload": "NORMAN_SET_REMINDER"},
            {"content_type": "text", "title": "Request Urgent Help", "payload": "NORMAN_REQUEST_URGENT_HELP"},
            {"content_type": "text", "title": "Book an Appointment","payload": "NORMAN_BOOK_APPOINTMENT"}
        ]
        self.send_message("text", message_text=message_text,quick_replies=quick_replies)
        return response.response_ok('Success')

    def good_to_go(self):
        message_text = "Awesome {0}".format(MessageConfig.EMOJI_DICT['HAPPY_SMILE'])
        self.send_message("text", message_text=message_text)
        response.response_ok('Success')
        self.beyondGetStarted()
        return response.response_ok('Success')

    def beyondGetStarted(self):
        if self.current_user.is_from_ref_id:
            message_text = MessageConfig.COMING_FROM_HOSPITAL
            self.show_typing('typing_on')
            self.show_typing('typing_off')
            self.send_message('text', message_text)
            self.show_typing('typing_on')
            self.show_typing('typing_off')
            self.send_message('text', MessageConfig.TIME_TO_SET_UP)
            response.response_ok('Success')
        else:
            self.handle_first_time_temp_user()

    def handle_first_time_temp_user(self):
        for statement in MessageConfig.FIRST_TIME_TEMP_USER:
            self.send_message('text', statement)
        quick_replies = [
            {"content_type": "text", "title": "Get Nearby Hospital", "payload": "GET_NEARBY_HOSPITAL"}
        ]
        text = "While you can enjoy some of my services as a free user," + " to enjoy the best of my features, you need to be registered to an hospital."
        self.send_message("text", message_text=text, quick_replies=quick_replies)
        return response.response_ok('Success')

    @property
    def handle_messaging_service(self):
        message_text = "Who would you like to leave a message for?"
        self.send_message("text", message_text=message_text)
        """
            Hey lekan my laptop is about to go off,
            @Todo: Here is what i am trying to do here
            1. Create a boolean field 'awaiting_message' in the user model
            1. At this point, update field to true
            2. When  a new message comes in from the same user, check if the user's
              awaiting_message is true
            3. take the message as continuation of the previous message
        """
        MessagingService.add_previous_message()
        return response.response_ok('Success')

    def handle_awaited_message(self, message_type='messaging_service'):
        if message_type == 'messaging_service':
            if 'users_last_message was a reponse to who?':
                message_text = "What message would you like to leave a message?"
                self.send_message("text", message_text=message_text)
            elif 'users_last_message_was a response to what':
                MessagingService.send_notification(who='previous_message', what='this_message')
                message_text = "Your message was successfully sent"
                self.send_message("text", message_text=message_text)
        else:
            message_text = "Sorry, I didn't get that, let's try again"
            self.send_message("text", message_text=message_text)

    def handle_api_ai_message(self, message):
        test = AI()
        test.parse(message)
        if test.match_successful:
            reply = test.text
            self.send_message('text', message_text=reply)
        else:
            reply = "Sorry I didn't get that, let's try again"
            self.send_message('text', message_text=reply)

        return response.response_ok('Success')

    def handle_leave_message(self):
        pass

    def handle_set_reminder(self):
        pass

    def handle_request_urgent_help(self):
        pass

    def handle_book_appointment(self):
        pass

    def handle_get_nearby_hospital(self):
        pass
