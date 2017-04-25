from flask import json


def get_request_type(payload):
    data = json.loads(payload)
    if "postback" in data["entry"][0]["messaging"][0]:
        return "postback"

    elif "message" in data["entry"][0]["messaging"][0]:
        return "message"


def postback_events(payload):
    data = json.loads(payload)

    postbacks = data["entry"][0]["messaging"]

    for event in postbacks:
        sender_id = event["sender"]["id"]
        postback_payload = event["postback"]["payload"]
        yield sender_id, postback_payload