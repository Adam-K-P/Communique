from __future__ import print_function

import boto3
import json

from boto3.dynamodb.conditions import Key, Attr

DB_NAME = 'communiquePhoneDB'
PRM_KEY = 'user_email'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DB_NAME)

def is_in_table(event):
     return table.query(KeyConditionExpression=Key(PRM_KEY).eq(event[PRM_KEY]))['Items']
     
def add_phone_number(event):
    table.put_item(
        Item = {
            PRM_KEY: event[PRM_KEY],
            'phone_number': event['phone_number']
        }
    )
                            
def update_phone_number(event):
    table.update_item(
        Key = {
            PRM_KEY: event[PRM_KEY]
        },
        UpdateExpression = 'SET phone_number = :vall',
        ExpressionAttributeValues = {
            ':vall': event['phone_number']
        }
    )

def lambda_handler(event, context):
    if is_in_table(event): update_phone_number(event)
    else: add_phone_number(event)
    return 'ok'
   
    
