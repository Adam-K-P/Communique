import boto3
import logging, sys
import io
from boto3.dynamodb.conditions import Key, Attr

_LOG_FILE = '/home/ubuntu/ec2_process/debug_log'

logging.basicConfig(filename = _LOG_FILE, level=logging.DEBUG)

_POST_DB_NAME  = 'communiqueDB'
_PHONE_DB_NAME = 'communiquePhoneDB'

_POST_DB  = boto3.resource('dynamodb').Table(_POST_DB_NAME)
_PHONE_DB = boto3.resource('dynamodb').Table(_PHONE_DB_NAME)

_SNS = boto3.client('sns')

def scan_post_db():
   return _POST_DB.scan()

def _delete_notification(item):
   _POST_DB.delete_item(
         Key = {
            'id': item['id']
         }
   )
   
def send_notification(item):
   phone_item = _is_in_table(item)
   if phone_item: _SNS.publish(PhoneNumber = phone_item[0]['phone_number'],
                               Message = item['message'])
   _delete_notification(item)

def _is_in_table(item):
   return _PHONE_DB.query(KeyConditionExpression = 
                          Key('user_email').eq(item['user_email']))['Items']


