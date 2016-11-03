#!/usr/bin/python

import boto3
import time
import datetime
from pytz import timezone

client = boto3.client('dynamodb')

DB_NAME = 'communiqueDB'

DAY_MAP = dict(MON = 0,
               TUE = 1,
               WED = 2,
               THU = 3,
               FRI = 4,
               SAT = 5,
               SUN = 6)

#max number of minutes that a notification is valid after its scheduled time
MAX_SLACK_TIME = 5

def _scan_db():
    return client.scan(TableName = DB_NAME)

def _parse_message_time(item):
    day_time = item['time']['S']
    return (day_time[0:3], int(day_time[3:5]), int(day_time[5:7]))

#TODO: use the appropriate timezone for each person
def _get_current_datetime():
    dt = datetime.datetime.now(timezone('US/Pacific'))
    return (dt.weekday(), dt.hour, dt.minute)

def _send_notification(item):
    print 'send notification'

def _delete_notification(item):
    print 'delete notification'

'''
We send a notification if the day, hour and minute are equal to the current
day, hour and minute or if they are close enough that it could reasonably be
a latency issue (we define it as MAX_SLACK_TIME).  We delete the notification
if it is too far passed to be considered valid (greater than MAX_SLACK_TIME)

The function is dirty, but it's ultimately just easier to leave all the
conditionals together rather than breaking them up

Good lord I need to unit test the f%ck out of this function
'''
def _should_send_notification(item):
    notf_weekday, notf_hour, notf_minute = _parse_message_time(item)
    curr_weekday, curr_hour, curr_minute = _get_current_datetime()
    if DAY_MAP[notf_weekday] == curr_weekday:
        if curr_hour == notf_hour:
            if curr_minute == notf_minute:
                _send_notification(item)
            elif notf_minute < curr_minute:
                if curr_minute - not_minute <= MAX_SLACK_TIME:
                    _send_notification(item)
                else: _delete_notification(item)
        elif notf_hour < curr_hour:
            if notf_hour == curr_hour - 1:
                if 60 - notf_minute + curr_minute <= MAX_SLACK_TIME:
                    _send_notification(item)
                else: _delete_notification(item)
            else: _delete_notification(item)
    elif (DAY_MAP[notf_weekday] < curr_weekday or
          DAY_MAP[notf_weekday] == 6 and curr_weekday == 0):
        if curr_hour == 0 and notf_hour == 23:
            if 60 - notf_minute + curr_minute <= MAX_SLACK_TIME:
                _send_notification(item)
            else: _delete_notification(item)
        else: _delete_notification(item)

def _polling_loop():
    while True:
        map(_should_send_notification, 
            filter(lambda item: 'time' in item, _scan_db()['Items']))
        time.sleep(60)

def __main():
    _polling_loop()

__main()

