import boto3

_SNS = boto3.client('sns')

_MY_PHONE_NUMBER = '+14088878783'

'''
db structures is gonna have to change
need to keep the notification in there after it's sent for some period of time (1 hour? a day?)
i need another field (sent field)
can also be used for repeatable notifications?
'''

def __main(event, context):
    message = 'Received message from: ' + event['from'] + ' with body: ' + event['body']
    _SNS.publish(PhoneNumber=_MY_PHONE_NUMBER, Message=message)

