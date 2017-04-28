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
            "image_url": "https://wallpaperbrowse.com/media/images/pictures-14.jpg",
            "subtitle": "100% Cotton, 200% Comfortable",
            "default_action": {
                "type": "web_url",
                "url": "https://norman-bot.herokuapp.com/",
                "messenger_extensions": True,
                "webview_height_ratio": "tall",
                "fallback_url": "https://norman-bot.herokuapp.com/"
            },
            "buttons": [
                {
                    "title": "Shop Now",
                    "type": "web_url",
                    "url": "https://norman-bot.herokuapp.com/",
                    "messenger_extensions": True,
                    "webview_height_ratio": "tall",
                    "fallback_url": "https://norman-bot.herokuapp.com/"
                }
            ]
    }


    t.send_template_message(template_type='list', list_info=[list_item_one, list_item_two])

    Notes:
        1. Maximum of 4 elements and minimum of 2 elements
        2. Maximum of 1 button per element
        3. All urls used must be registered in FBConfig.WHITE_LISTED_DOMAINS
            ** You must explicitly run utils.update_white_listed_domains() after
                adding a url for the changes to take effect as it is not called automatically
        4. Urls must be https
    """



if __name__ == '__main__':
    t = Template('1280106375410348')
    list_item_one = {
        "title": "Classic White T-Shirt",
        "image_url": "https://wallpaperbrowse.com/media/images/pictures-14.jpg",
        "subtitle": "100% Cotton, 200% Comfortable",
        "default_action": {
            "type": "web_url",
            "url": "https://norman-bot.herokuapp.com/",
            "messenger_extensions": True,
            "webview_height_ratio": "tall",
            "fallback_url": "https://norman-bot.herokuapp.com/"
        },
        "buttons": [
            {
                "title": "Shop Now",
                "type": "web_url",
                "url": "https://norman-bot.herokuapp.com/",
                "messenger_extensions": True,
                "webview_height_ratio": "tall",
                "fallback_url": "https://norman-bot.herokuapp.com/"
            }
        ]
    }
    print(t.send_template_message(template_type='list', list_info=[list_item_one, list_item_one]))
