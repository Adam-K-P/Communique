import time
import datetime
from pytz import timezone

import aws_util
import settings

DAY_MAP = dict(MON = 0,
               TUE = 1,
               WED = 2,
               THU = 3,
               FRI = 4,
               SAT = 5,
               SUN = 6)

#max number of minutes that a notification is valid after its scheduled time
#set it to 5 on testing so that debugging is easier
MAX_SLACK_TIME = 5 if settings._TEST else 2

def _parse_message_time(item):
    day_time = item['time']
    return (day_time[0:3], int(day_time[3:5]), int(day_time[5:7]))

#TODO: use the appropriate timezone for each person
def _get_current_datetime():
    dt = datetime.datetime.now(timezone('US/Pacific'))
    return (dt.weekday(), dt.hour, dt.minute)

'''
We send a notification if the day, hour and minute are equal to the current
day, hour and minute or if they are close enough that it could reasonably be
a latency issue (we define it as MAX_SLACK_TIME).  If it is outside of this
MAX_SLACK_TIME range, then we'll just assume it's for next week.
'''
def should_send_notification(item):
    notf_weekday, notf_hour, notf_minute = _parse_message_time(item)
    curr_weekday, curr_hour, curr_minute = _get_current_datetime()
    if DAY_MAP[notf_weekday] == curr_weekday:
        if curr_hour == notf_hour:
            if curr_minute == notf_minute:
                aws_util.send_notification(item)
            elif notf_minute < curr_minute:
                if curr_minute - notf_minute <= MAX_SLACK_TIME:
                    aws_util.send_notification(item)
        elif notf_hour < curr_hour:
            if notf_hour == curr_hour - 1:
                if 60 - notf_minute + curr_minute <= MAX_SLACK_TIME:
                    aws_util.send_notification(item)
    elif (DAY_MAP[notf_weekday] < curr_weekday or
          DAY_MAP[notf_weekday] == 6 and curr_weekday == 0):
        if curr_hour == 0 and notf_hour == 23:
            if 60 - notf_minute + curr_minute <= MAX_SLACK_TIME:
                aws_util.send_notification(item)

