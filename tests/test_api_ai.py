from Norman.api.api_ai import Agent
from Norman.utils import generate_session_id


def test_ai():

    sample_sentence = "i'll like to leave a message?"
    result = Agent.parse(sample_sentence, session_id=generate_session_id())
    expected_result = 'messaging', 'messaging', True, 'who would you like to leave a message for?'

    print('sample sentence: ', sample_sentence)
    print('result: ', result)
    print('expected result: ', expected_result)
    print('Test passed: ', result == expected_result)

if __name__ == '__main__':
    test_ai()
