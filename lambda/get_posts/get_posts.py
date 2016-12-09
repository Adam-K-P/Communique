from __future__ import print_function

import boto3
import json

client = boto3.client('dynamodb')

DB_NAME = 'communiqueDB'

def __main(event, context):
    if event['limit'] != '': 
        return client.scan(TableName=DB_NAME, Limit=int(event['limit']))
    return client.scan(TableName=DB_NAME)
