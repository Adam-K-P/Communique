import requests

import urllib3.contrib.pyopenssl
import json
 
urllib3.contrib.pyopenssl.inject_into_urllib3()

AWS_BASE_URL = "https://66qgd1ph4a.execute-api.us-east-1.amazonaws.com/prod/"
AWS_ADD_POST_URL = AWS_BASE_URL + "addpost"
AWS_GET_POSTS_URL = AWS_BASE_URL + "getposts"
AWS_HAS_PHONE_NUMBER_URL = AWS_BASE_URL + "hasphonenumber"
AWS_ADD_PHONE_URL = AWS_BASE_URL + "addphone"

def _get_proper_hour(hour, am):
    if int(am) == 0: return '00' if int(hour) == 12 else hour
    else: return '12' if int(hour) == 12 else str(int(hour) + 12)

def _get_proper_time(time):
    day = time[0:3]
    hour = _get_proper_hour(time[3:5], time[7:8])
    minute = time[5:7]
    return day + hour + minute

@auth.requires_signature()
def add_notf():
    request_data = {
        "time": _get_proper_time(request.vars.time),
        "user_email": request.vars.user_email,
        "message": request.vars.message
    }
    headers = {'Content-type': 'application/json'}
    requests.post(AWS_ADD_POST_URL, headers=headers,
                  data=json.dumps(request_data))
    return "ok"

@auth.requires_signature()
def get_notfs():
    headers = {'Content-type': 'application/json'}
    return response.json(dict(notifications = 
                              _get_notfs(requests.get(AWS_GET_POSTS_URL,
                                         params = {
                                            'user_email':request.vars.user_email
                                         },
                                         headers=headers).json())))

@auth.requires_signature()
def has_phone_number():
    headers = {'Content-type': 'application/json'}
    return requests.get(AWS_HAS_PHONE_NUMBER_URL, headers=headers,
                        params = {
                            'user_email':request.vars.user_email
                        }).json()

@auth.requires_signature()
def add_phone_number():
    headers = {'Content-type': 'application/json'}
    request_data = {
        'user_email': request.vars.user_email,
        'phone_number': request.vars.phone_number
    }
    requests.post(AWS_ADD_PHONE_URL, headers=headers, 
                  data=json.dumps(request_data))
    return 'ok'

def _get_notfs(response):
    return map(_strip_notfs, 
               filter(lambda item: 'message' in item, response['Items']))
    
def _strip_notfs(item):
    return dict(message = item['message']['S'],
                time = item['time']['S'])
