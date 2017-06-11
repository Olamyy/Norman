import json
from socket import gaierror

from apiai import ApiAI

from Norman.errors import HttpError
from Norman.settings import ApiAIConfig
from Norman.utils import generate_session_id

ai = ApiAI(ApiAIConfig.CLIENT_ACCESS_TOKEN)


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
    message = 'hi'
    test.parse(message)
    if test.match_successful:
        reply = test.text
        print(reply)
    else:
        pass

