import boto3

_POST_DB_NAME = 'communiqueDB'

_POST_DB = boto3.resource('dynamodb').Table(_POST_DB_NAME)

def delete_post(id):
    _POST_DB.delete_item(
        Key = {
            'id': id
        }
    )

def __main(event, context):
    delete_post(event['id'])
    return 'ok'
