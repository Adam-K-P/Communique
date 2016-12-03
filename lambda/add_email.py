import boto3

SES = boto3.client('ses')

def lambda_handler(event, context):
    response = SES.verify_email_identity(EmailAddress=event['user_email'])
    return 'ok'
