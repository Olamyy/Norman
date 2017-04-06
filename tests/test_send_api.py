from Norman.messenger.sendAPI import Message, Template

m = Message('1280106375410348')
m.send_action('typing_on')

#
#   "recipient":{
#   	"id":"USER_ID"
#   },
#   "sender_action":"typing_on"
# }'