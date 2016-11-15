#!/usr/bin/python

import time
import datetime
from pytz import timezone
import os

import aws_util
import notifier
import settings

_MAX_POLLING_ATTEMPTS = 5

#determines how long we wait till we start the next polling loop
#helps determine whether we can actually recover from an error
_POLLING_BACKOFF_CONSTANT = 20 #linear backoff

def _perform_scan():
    try:
        scan = aws_util.scan_post_db()
        return scan['Items']
    except Exception, e:
        settings.log("Encountered exception while performing scan_post_db", e)
        return []

def _polling_loop():
    while True:
        map(notifier.should_send_notification,
            filter(lambda item: 'time' in item, _perform_scan()))
        time.sleep(60)

def __main(polling_attempts):
    if polling_attempts == 0:
        if os.fork() != 0: exit() #damonize
        settings.init()

    try:
        _polling_loop()

    except Exception, e:
        exception_message = (
                "Exception encountered while performing polling loop\n"
                "This is polling attempt #" + 
                str(polling_attempts) + "\n"
        )
        if polling_attempts == _MAX_POLLING_ATTEMPTS:
            exception_message += (
                "There have been too many polling attempts, now exiting"
            )
            settings.log(exception_message, e)
            exit(1)

        else:
            exception_message += (
                "Attempting polling loop again after backoff of: " +
                str(polling_attempts * _POLLING_BACKOFF_CONSTANT) + 
                " seconds"
            )
            settings.log(exception_message, e)
            time.sleep (polling_attempts * _POLLING_BACKOFF_CONSTANT)
            __main(++polling_attempts)

__main(0)

