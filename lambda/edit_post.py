import boto3

_POST_DB_NAME = 'communiqueDB'

_POST_DB = boto3.resource('dynamodb').Table(_POST_DB_NAME)

def update_message(post_id, message):
    _POST_DB.update_item(
        Key = {
            'id': post_id
        },
        UpdateExpression = 'SET message = :vall',
        ExpressionAttributeValues = {
            ':vall': message
        }
    )
    
def update_time(post_id, time_):
    _POST_DB.update_item(
        Key = {
            'id': post_id
        },
        UpdateExpression = 'SET #time__ = :vall',
        ExpressionAttributeValues = {
            ':vall': time_
        },
        ExpressionAttributeNames = {
            '#time__': 'time'
        }
    )
    
def update_delivery_method(post_id, delivery_method):
    _POST_DB.update_item(
        Key = {
            'id': post_id
        },
        UpdateExpression = 'SET delivery_method = :vall',
        ExpressionAttributeValues = {
            ':vall': delivery_method
        }
    )
    
def update_post(event):
    if 'message' in event: update_message(event['id'], event['message'])
    if 'time' in event: update_time(event['id'], event['time'])
    if 'delivery_method' in event: update_delivery_method(event['id'], event['delivery_method'])
            
def lambda_handler(event, context):
    update_post(event)
    return 'ok'
