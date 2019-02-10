"""This file will handle all calls to Twilio's API (the proxy services)"""

from twilio.rest import Client

import twilioAuth  # contains API authentication variables

client = Client(twilioAuth.accountSID, twilioAuth.authToken)

# phoneNumber = client.proxy.services(twilioAuth.serviceID).phone_numbers.create(sid=twilioAuth.phoneSID)

# session = client.proxy.services(twilioAuth.serviceID).sessions.create(unique_name="HackDavis2019 Session")

"""Add participants"""
# participant0 = client.proxy \
#                     .services(twilioAuth.serviceID) \
#                     .sessions(twilioAuth.sessionID) \
#                     .participants \
                    # .create(friendly_name='test0', identifier=twilioAuth.partipcant0Number)

# participant1 = client.proxy \
#                     .services(twilioAuth.serviceID) \
#                     .sessions(twilioAuth.sessionID) \
#                     .participants \
                    # .create(friendly_name='test0', identifier=twilioAuth.particpant1Number)

"""See list of partipcants"""
# participants = client.proxy \
#                      .services(twilioAuth.serviceID) \
#                      .sessions(twilioAuth.sessionID) \
#                      .participants \
#                      .list()

# for record in participants:
#     print(record.sid)


message_interaction = client.proxy \
    .services(twilioAuth.serviceID) \
    .sessions(twilioAuth.sessionID) \
    .participants(twilioAuth.participant1) \
    .message_interactions \
    .create(body='Call this anonymized number to remind NAME about REMINDER!')

print(message_interaction.sid)