from Norman.settings import Config
from Norman.api.base import base
from Norman.errors import HttpError


class ProfileAPI:
    # @Todo : Handle Delete URLs
    def __init__(self):
        self.field_name = ''
        self.graphAPIURL = Config.GRAPH_API_URL.replace('<action>', '/me/messenger_profile')
        self.graphAPIURLFields = Config.GRAPH_API_URL.replace('<action>', 'me/messenger_profile?'
                                                                          'fields={0}'.format(self.field_name))


class PersitentMenu(ProfileAPI):
    """
    Setting, Getting and Deleting Persistent Menu.
    Make sure you read and understand this very well for sending the data :
    https://developers.facebook.com/docs/messenger-platform/messenger-profile/persistent-menu
    """
    def __init__(self):
        super().__init__()
        self.field_name = 'persistent_menu'

    def set_menu(self, menu_data):
        """
        https://developers.facebook.com/docs/messenger-platform/messenger-profile/persistent-menu has a detailed documentation
        on the menu data and formats.
        :param menu_data:
        :return:
        """
        request = base.exec_request('POST', self.graphAPIURL, data=menu_data)
        if request:
            print("Successfully Set Menu")

    def get_menu(self):
        request = base.exec_request('GET', self.graphAPIURLFields)
        if request:
            return request

    def delete_menu(self):
        request = base.exec_request('DELETE', self.graphAPIURLFields)
        if request:
            return request


class GetStarted(ProfileAPI):
    """
    Setting, Getting and Deleting Persistent Menu.
    Make sure you read and understand this very well for sending the data:
    https://developers.facebook.com/docs/messenger-platform/messenger-profile/get-started-button
    """
    def __init__(self):
        super().__init__()
        self.field_name = "get_started"

    def set_message(self, payload):
        request = base.exec_request('POST', self.graphAPIURL, data=payload)
        if request:
            print(request)
        else:
            raise HttpError('Unable to complete request.')

    def get_message(self):
        request = base.exec_request('GET', self.graphAPIURLFields)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')

    def delete_message(self):
            request = base.exec_request('DELETE', self.graphAPIURLFields)
            if request:
                return request
            else:
                raise HttpError('Unable to complete request.')


class GreetingText(ProfileAPI):
    """
    Setting, Getting and Deleting Persistent Menu.
    Make sure you read and understand this very well for sending the data :
    https://developers.facebook.com/docs/messenger-platform/messenger-profile/greeting-text
    """
    def __init__(self):
        super().__init__()
        self.field_name = "greeting"

    def set_text(self, payload):
        request = base.exec_request('POST', self.graphAPIURL, data=payload)
        if request:
            print(request)
        else:
            raise HttpError('Unable to complete request.')

    def get_text(self):
        request = base.exec_request('GET', self.graphAPIURLFields)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')

    def delete_message(self):
        request = base.exec_request('DELETE', self.graphAPIURLFields)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')


class WhitelistDomain(ProfileAPI):
    def __init__(self):
        super().__init__()
        self.field_name = "whitelisted_domains"

    def set_text(self, payload):
        request = base.exec_request('POST', self.graphAPIURL, data=payload)
        if request:
            print(request)
        else:
            raise HttpError('Unable to complete request.')

    def get_text(self):
        request = base.exec_request('GET', self.graphAPIURLFields)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')

    def delete_message(self):
        request = base.exec_request('DELETE', self.graphAPIURLFields)
        if request:
            return request
        else:
            raise HttpError('Unable to complete request.')


class AccountLinking(ProfileAPI):
    """
    Not sure if we need this now but let's just leave it here.
    """
    pass

    
class TargetAudience(ProfileAPI):
    """
    Not sure if we need this now but let's just leave it here.
    """
    pass


