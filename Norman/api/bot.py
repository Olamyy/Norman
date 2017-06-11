from flask import Blueprint
from flask import make_response
from flask import request
from flask_restful import Resource

from Norman.api.web import UserAPI
from Norman.extensions import csrf_protect
from Norman.messenger.Utils import get_request_type, postback_events
from Norman.messenger.payloadconversation import PayloadConversationHandler
from Norman.norman.user import NormanUser
from Norman.utils import response

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
        if request_type == 'postback':
            for recipient_id, postback_payload, referral_load in postback_events(data):
                print('The ref is', referral_load)
                if referral_load:
                    self.normanuser.update_ref_id(referral_load, recipient_id)
                    payloadhandler = PayloadConversationHandler(registered=True, recipient_id=recipient_id)
                    return payloadhandler.handleconversation(postback_payload)
                print('No reffereal')
                payloadhandler = PayloadConversationHandler(registered=False, recipient_id=recipient_id)
                return payloadhandler.handleconversation(postback_payload)
            return response.response_ok('success')

        elif request_type == "message":
            print(request_type)
            return response.response_ok('success')

        else:
            return response.response_ok('success')
