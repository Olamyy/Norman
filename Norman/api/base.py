import json

import requests

from Norman.errors import HttpMethodError


class BaseAPI(object):
    """

    """

    _content_type = "application/json"

    def __init__(self):
        pass

    def _json_parser(self, json_response):
        response = json_response.json()
        return response

    def exec_request(self, method, url, data=None):
        method_map = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete
        }

        payload = data if data else data
        request = method_map.get(method)

        if not request:
            raise HttpMethodError(
                "Request method not recognised or implemented")

        response = request(
            url=url, json=payload, verify=True)

        return response.content

        # if response.status_code == 404:
        #     msg = "The object request cannot be found"
        #     if response.json().get('message'):
        #         body = response.json()
        #     return response.status_code, body
        #     # return response.status_code, False, msg, None
        # body = response.json()
        # if body.get('status') == 'error':
        #     return response.status_code, body['status'], body['message']
        # if response.status_code in [200, 201]:
        #     return self._json_parser(response)
        # response.raise_for_status()

base = BaseAPI()