import boto3
from boto3.dynamodb.conditions import Key, Attr

_POST_DB_NAME  = 'communiqueDB'
_PHONE_DB_NAME = 'communiquePhoneDB'

_POST_DB  = boto3.resource('dynamodb').Table(_POST_DB_NAME)
_PHONE_DB = boto3.resource('dynamodb').Table(_PHONE_DB_NAME)

_SNS = boto3.client('sns')
_SES = boto3.client('ses')

_SEND_EMAIL = '"Communique" <communique.notifier@mail.com>'

_SUBJECT = 'Notification from Communique!'
_CHARSET = 'utf-8'

def scan_post_db():
   return _POST_DB.scan()

def _delete_notification(item):
   _POST_DB.delete_item(
         Key = {
            'id': item['id']
         }
   )
   
def send_notification(item):
   try:
      '''
      phone_item = _is_in_table(item)
      if phone_item: _SNS.publish(PhoneNumber = phone_item[0]['phone_number'],
                                  Message = item['message'])
      '''
      _send_email_notification(item)
      _delete_notification(item)

   except Exception, e:
      settings.log("Encountered exception while trying to send notification" +
                   "\nException Message: " + str(e))

def _produce_html(item):
   return '<p>' + item['message'] + '</p>'

def _send_email_notification(item):
   response = _SES.send_email(Source=_SEND_EMAIL,
                                 Destination= {
                                    'ToAddresses': [
                                       item['user_email']
                                    ]
                                 },
                                 Message= {
                                    'Subject' : {
                                       'Data' : _SUBJECT,
                                    },
                                    'Body': {
                                       'Text': {
                                          'Data': item['message'],
                                       },
                                       'Html' : {
                                          'Data' : _produce_html(item)
                                       }
                                    }
                                 }
                              )

def _is_in_table(item):
   try:
      query = _PHONE_DB.query(KeyConditionExpression = 
                             Key('user_email').eq(item['user_email']))['Items']
   except Exception, e:
      settings.log("Exception encountered while checking for item in table" +
                   "Exception message: " + str(e))
      return False


