from __future__ import print_function

import boto3
import json

from boto3.dynamodb.conditions import Key, Attr

DB_NAME = 'communiquePhoneDB'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DB_NAME)

def __main(event, context):
    return table.scan()
