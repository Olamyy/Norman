from Norman.messenger.sendAPI import Message, Template


"""
    Examples on how to you sendAPI class in your code
"""

def test_message(recipient):
    """

    :param recipient: a valid recipient id
    :return: a json response from the server

    - Message.send_action: Sends an action to the recipient.
        :param  "typing_on", "typing_off" or "mark_seen"

    - Message.send_message: Sends a text message or an attachment
         :param message_type: "text" or "attachment"
         :param message_text: 'Replace this with the text to send to recipient'
         :param attachment: Must be a valid attachment object.
                            Valid attachment files types are: file, image, audio and video.
                            Check example below for structure.(optional)
         :param notication_type: "REGULAR", "SILENT_PUSH", or "NO_PUSH"(optional)
         :param quick_replies:

    *** EXAMPLES / SAMPLE USAGE ***

    # Send a plain text reply
    >>> m = Message('some_fb_user_id')
    >>> m.send_message(message_text='Hello, World!') # simple message

    # Send an attachment
    >>> m.send_message(message_text='attachment',
                       attachment = {
                                     'type': 'file',
                                     "payload":{"url":"https://petersapparel.com/bin/receipt.pdf"},
                                    },
                       )

    # Send a user action
    >>> m.send_action('typing_on')

    # Send a quick reply
    >>> m.send_message(message_type='text', message_text='Are you sure you want to remove the service?',
                       quick_replies = [
                                        {"content_type":"text", "title":"Confirm", "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"},
                                        {"content_type":"text", "title":"Cancel", "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"}
                                        ]
                         )


    # send a list_template

    >>> list_item_one = {
                    "title": "Classic White T-Shirt",
                    "image_url": "https://peterssendreceiveapp.ngrok.io/img/white-t-shirt.png",
                    "subtitle": "100% Cotton, 200% Comfortable",
                    "default_action": {
                        "type": "web_url",
                        "url": "https://peterssendreceiveapp.ngrok.io/view?item=100",
                        "messenger_extensions": true,
                        "webview_height_ratio": "tall",
                        "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                                     },
                    "buttons": [
                        {
                            "title": "Shop Now",
                            "type": "web_url",
                            "url": "https://peterssendreceiveapp.ngrok.io/shop?item=100",
                            "messenger_extensions": true,
                            "webview_height_ratio": "tall",
                            "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                        }
                    ]
                }

    """






# m = Message('1280106375410348')
# m.send_message(message_type='attachment',
#                attachment={
#                                      'type': 'image',
#                                      "payload": {"url": "https://avatars2.githubusercontent.com/u/14059714?v=3&s=460"},
#                            },
#                )






# m = Message('1280106375410348')
# print(m.send_message(message_type='text', message_text='Are you sure you want to remove the service?',
#                quick_replies=[
#                               {"content_type":"text", "title":"Confirm", "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"},
#                               {"content_type":"text", "title":"Cancel", "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"}
#                              ]
#                ))







    #
    # """
    #     1. Message.send_message()
    #     2. Message.send_action
    # """
    # Message.send_message()
    #
    #
    # if response:
    #     # do something
    #     pass
    # else:
    #     # do something else
    #     pass

# def test_template(recipient):
#     t = Template('1280106375410348')
#
# para = {
#     'title': 'Get Started',
#     'type': 'web_url',
#     'url': 'https://norman-bot.herukoapp.com',
# }
#
# print(t.send_template_message(template_type='button', text='Welcome to Norman. Please visit the website to get started',
#                         buttons=para))














#{
#   "recipient":{
#   	"id":"USER_ID"
#   },
#   "sender_action":"typing_on"
# }'

# https://graph.facebook.com/v2.6/me/messages?access_token=EAAS0PtgoBk4BAKIZBKELBTB7JZBsoetjvG1A3xmMWhJFlDxeUtfgNgr2odxHZBqZAailae0ev0PaIzLz7ifaWEAfIKTfWGy35yjejmzA9OJVhH2mxMPNGXzBhE397hWZBJhP8Uz0uJ588lJ4jW5DQN0544Gq1d7BuqYBAxflaiQZDZD
# https://graph.facebook.com/v2.6/me/messages?access_token=EAAS0PtgoBk4BAKIZBKELBTB7JZBsoetjvG1A3xmMWhJFlDxeUtfgNgr2odxHZBqZAailae0ev0PaIzLz7ifaWEAfIKTfWGy35yjejmzA9OJVhH2mxMPNGXzBhE397hWZBJhP8Uz0uJ588lJ4jW5DQN0544Gq1d7BuqYBAxflaiQZDZD"

# "recipient":{
#   "id":"1280106375410348"
#   },
#   "sender_action": "typing_on"
# }

# "{"recipient":{"id":"USER_ID"}, "message":{"text":"hello, world!"}}"

# "{
#   "recipient":{
#   	"id":"1280106375410348"
#   },
#   "message":{
#   	"text":"hello, world!"
#   }
# }"
#
# curl -X POST -H "Content-Type: application/json" -d '{
#   "recipient":{
#   	"id":"1280106375410348"
#   },
#   "sender_action":"typing_on"
# }' "https://graph.facebook.com/v2.6/me/messages?access_token=EAAS0PtgoBk4BAKIZBKELBTB7JZBsoetjvG1A3xmMWhJFlDxeUtfgNgr2odxHZBqZAailae0ev0PaIzLz7ifaWEAfIKTfWGy35yjejmzA9OJVhH2mxMPNGXzBhE397hWZBJhP8Uz0uJ588lJ4jW5DQN0544Gq1d7BuqYBAxflaiQZDZD"
#
#
# '{"recipient": {"id":"1280106375410348"}, "sender_action":"typing_on"}'
# '{"recipient": {"id":"1280106375410348"}, "message":{"text":"hello, world!"}}'
# '{"recipient": {"id":"1280106375410348"}, "message":{"text":"typing_on"}}'
# '{"recipient": {"id": "1280106375410348"}, "message": {"text": "typing_on"}}'