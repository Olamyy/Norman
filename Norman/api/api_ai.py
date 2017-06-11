import json
from socket import gaierror

from apiai import ApiAI

from Norman.errors import HttpError
from Norman.settings import ApiAIConfig
from Norman.utils import generate_session_id

ai = ApiAI(ApiAIConfig.CLIENT_ACCESS_TOKEN)


<<<<<<< HEAD
class AI:
    def __init__(self):
        self.request = ai.text_request()
        self.request.lang = 'de'  # optional, default value equal 'en'
        self.request.session_id = generate_session_id()
        self.match_successful = False
        self.text = None

    def parse(self, data):
        print('got to apiai parse function')
        self.request.query = data
        try:
            r = self.request.getresponse()  # returns a response object
            response = json.loads(r.read().decode(encoding='UTF-8').replace('\n', ''))
            print(response)
        except HttpError:
            self.log.log_error('HTTP Error: Unable to complete request.')
            return
        except gaierror as e:
            self.log.log_error('Socket Error: {}'.format(e))
            return

        try:
            if response['result']['metadata']['intentName'] != 'Default Fallback Intent':
                self.match_successful = True
                self.text = response['result']['fulfillment']['speech']
        except KeyError:
            try:
                if response['result']['metadata'] == {}:
                    self.match_successful = True
                    self.text = response['result']['fulfillment']['speech']
            except KeyError:
                self.match_successful = False

if __name__ == '__main__':
    test = AI()
    message = "i'll like to leave a message"
    test.parse(message)
    if test.match_successful:
        reply = test.text
        print(reply)
    else:
        pass

=======
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
>>>>>>> 10ae86a0096b7a8ef209857d9b6431190964acc2
