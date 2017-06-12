from flask import Blueprint
from flask import make_response
from flask import request
from flask_restful import Resource
from Norman.api.web import UserAPI
from Norman.extensions import csrf_protect
from Norman.messenger.Utils import get_request_type, postback_events, messaging_events
from Norman.messenger.payloadconversation import PayloadConversationHandler
from Norman.norman.user import NormanUser
from Norman.utils import response, decode_data
from Norman.norman.processor import Processor

blueprint = Blueprint('api', __name__, url_prefix='/api')


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
        self.message = None
        self.normanuser = NormanUser()

    @staticmethod
    def get():
        args = request.args
        verify_token = 'python_rocks'
        if args.get('hub.mode') == 'subscribe' and args.get('hub.verify_token') == verify_token:
            return make_response(args.get('hub.challenge').strip("\n\""))
        else:
            return response.response_error('Failed validation. Make sure the validation tokens match', args)

    def post(self):
        data = request.get_data()
        request_type = get_request_type(data)
        print(data)

        if request_type == 'postback':
            for recipient_id, postback_payload, referral_load in postback_events(data):
                print(recipient_id)
                if referral_load:
                    self.normanuser.update_ref_id(referral_load, recipient_id)
                    payloadhandler = PayloadConversationHandler(registered=True, recipient_id=recipient_id)
                    return payloadhandler.handleconversation(postback_payload)
                payloadhandler = PayloadConversationHandler(registered=False, recipient_id=recipient_id)
                return payloadhandler.handleconversation(postback_payload)
            return response.response_ok('success')

        elif request_type == "message":
            print('Got a me')
            for recipient_id, message in messaging_events(data):
                print(message, recipient_id)
                if not message:
                    return response.response_ok('Success')
                message = decode_data(message.get('data'))
                processor = Processor(sentence=message, recipient_id=recipient_id)
                return processor.process()
            return response.response_ok('success')

        else:
            return response.response_ok('success')
