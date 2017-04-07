from Norman.messenger.sendAPI import Message, Template


"""
    Examples on how to you sendAPI class in your code
"""


def class_message(recipient):
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
    """


def class_template(recipient):

    """
    t = Template('some_fb_user_id')

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

    t.send_template_message('template_type=list', list_info=[list_item_one])

    """
