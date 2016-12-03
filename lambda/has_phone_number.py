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

def lambda_handler(event, context):
    return bool(is_in_table(event))
