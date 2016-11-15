import logging

_TEST = True

#Have to be careful with logging, the file can easily get huge and there is not
#enough memory on the ec2 instance to just leave logging on when unattended.
#So we just make our own log file to avoid unnecessary messages being logged
#rather than use python's logging feature.
_LOG_FILE = './debug_log'

_LOG_FILE_ = None

#This should really only be used for exceptions
def log(string, exception = None):
   if exception: string += "\nException message: " + repr(e)
   _LOG_FILE_.write(string)

def init():
   global _TEST
   _TEST = _TEST
   _LOG_FILE_ = open(_LOG_FILE, 'w')

