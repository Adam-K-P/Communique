
m __future__ import print_function

import boto3
import json

from boto3.dynamodb.conditions import Key, Attr

DB_NAME = 'communiqueDB'
PRM_KEY = 'id'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DB_NAME)

def get_next_id():
    return table.query(KeyConditionExpression=Key(PRM_KEY).eq(0))['Items'][0]['next_id']
    
def update_next_id(next_id):
    table.update_item(
        Key = {
            PRM_KEY: 0
        },
        UpdateExpression = 'SET next_id = :vall',
        ExpressionAttributeValues = {
            ':vall': next_id
        }
    )
    
def place_item_in_db(id, info):
    table.put_item(Item = {
                            PRM_KEY: id,
                            'message': info['message'],
                            'time': info['time'],
                            'user_email': info['user_email'],
                            'delivery_method': info['delivery_method']
                          }
                  )
    update_next_id(id + 1)
    return id
                 
                                            
def lambda_handler(event, context):
   place_item_in_db(get_next_id(), event)
   return 'ok'
