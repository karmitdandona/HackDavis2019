from twilio.rest import Client

import twilioAuth

def SendCallMessage(targetID, targetName, reminder):
  """targetID is the twilio participant ID's. Sends"""
  client = Client(twilioAuth.accountSID, twilioAuth.authToken)
  
  message_interaction = client.proxy \
    .services(twilioAuth.serviceID) \
    .sessions(twilioAuth.sessionID) \
    .participants(targetID) \
    .message_interactions \
    .create(body='Call this anonymized number to remind ' + targetName + ': ' + reminder)

  return