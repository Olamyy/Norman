from apiai import ApiAI
import json
from Norman.settings import ApiAIConfig
from Norman.utils import generate_session_id
from Norman.errors import HttpError
from Norman.logger import Logger
from socket import gaierror


ai = ApiAI(ApiAIConfig.CLIENT_ACCESS_TOKEN)


class AI:
    def __init__(self):
        self.request = ai.text_request()
        self.request.lang = 'de'  # optional, default value equal 'en'
        self.request.session_id = generate_session_id()
        self.match_successful = False
        self.text = None
        self.log = Logger()

    def parse(self, data):
        self.request.query = data
        try:
            r = self.request.getresponse()  # returns a response object
            response = json.loads(r.read().decode(encoding='UTF-8').replace('\n', ''))
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
    test.parse('blahblahblah')
    if test.match_successful:
        print(test.text)
    else:
        print('Sorry couldn\'t match your input')
