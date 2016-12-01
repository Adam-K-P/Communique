import logging

_TEST = True

#Have to be careful with logging, the file can easily get huge and there is not
#enough memory on the ec2 instance to just leave python's logging on when 
#unattended. so we just make our own log file to avoid unnecessary messages 
#being logged
_LOG_FILE = open('./debug_log', 'w')

#This should really only be used for exceptions
def log(string, exception = None):
   if exception: string += "\nException message: " + repr(exception) + "\n"
   _LOG_FILE.write(string)

def init():
   global _TEST
   _TEST = _TEST

