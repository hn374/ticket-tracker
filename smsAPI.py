from twilio.rest import Client

class SmsAPI:
    # Constructor
    def __init__(self, accountId, authToken):
        self.accountId = accountId
        self.authToken = authToken
        self.client = Client(self.accountId, self.authToken)

    # Send sms text function
    def sendText(self, sendToNumber, sendFromNumber, content):
        message = self.client.messages.create(
            to=sendToNumber,
            from_=sendFromNumber,
            body=content)