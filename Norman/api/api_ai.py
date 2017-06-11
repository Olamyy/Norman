import json
from socket import gaierror

from apiai import ApiAI

from Norman.errors import HttpError
from Norman.logger import Logger
from Norman.settings import ApiAIConfig
from Norman.utils import generate_session_id

ai = ApiAI(ApiAIConfig.CLIENT_ACCESS_TOKEN)


class Agent:
    """
    An instance of our api.ai agent
    """
    @staticmethod
    def parse(sentence, session_id):
        """

        :param sentence: The sentence to parse (String)
        :param session_id: A unique identifier for each user
        :return: (serviceName, intentMatched, actionIncomplete, suggestedResponse)
                 service_name - this corresponds to the action specified under the intent matched
                 intent - this corresponds to the intent name on api.ai,
                 action_incomplete - (boolean) returns true if required slots are missing,
                 suggested_response - response filled on api.ai

        """

        request = ai.text_request()
        request.session_id = session_id
        request.query = sentence

        response = json.loads(request.getresponse().read().decode(encoding='UTF-8').replace('\n', ''))

        result = response['result']
        intent = response['result']['metadata']['intentName']
        service = result.get('action')
        action_incomplete = result.get('actionIncomplete', False)
        suggested_reply = response['result']['fulfillment']['speech']

        return service, intent, action_incomplete, suggested_reply
