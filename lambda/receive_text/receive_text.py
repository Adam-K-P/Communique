import boto3

_SNS = boto3.client('sns')

_MY_PHONE_NUMBER = '+14088878783'

def __main(event, context):
    _SNS.publish(PhoneNumber=_MY_PHONE_NUMBER, Message='Received message')

