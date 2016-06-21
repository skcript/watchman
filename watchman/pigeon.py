# -*- encoding: utf-8 -*-
import re
import time
import requests
import logging
from rratelimit import Limiter

# Modules in Watchman
from conf import load_endpoints, LOG_FILENAME, REDIS, RL_LIMIT, RL_PERIOD
import extension

ENDPOINTS = load_endpoints()
# Ratelimiter limiting pigeon at RL_LIMIT actions per RL_PERIOD
LIMITER = Limiter(REDIS, action='pigeon', limit=RL_LIMIT, period=RL_PERIOD)

# Logger Creds
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
log = logging.getLogger("watchman.pigeon")

# Ratelimiting server pings at RL_LIMIT actions per RL_PERIOD
def ratelimit():
    """
        This decorator ratelimits an API call based on string returned by
        extension.ratelimit()
    """
    def decorateRatelimit(func):
        def ratelimitFunction(*args,**kargs):
            name = extension.ratelimit(args[0])
            if name:
                while not LIMITER.checked_insert(name):
                    print "{0} is being rate limited".format(name)
                    time.sleep(0.5)

            ret = func(*args,**kargs)
            return ret

        return ratelimitFunction
    return decorateRatelimit

def dumpargs():
    """
        This decorator dumps out the arguments passed to a function before
        calling it
    """
    def decorateDumpargs(func):
        argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
        fname = func.func_name
        def dumpargsFunction(*args, **kargs):
            string = "Calling '" + fname + "' with args: " + ", ".join(
                                            '%s=%r' % entry
                                            for entry in zip(argnames, args[:len(argnames)])
                                        )
            print string
            log.debug(string)

            ret = func(*args, **kargs)
            return ret

        return dumpargsFunction
    return decorateDumpargs

def prevent():
    """
        This decorator prevents an API call by comparing boolean returned by
        extension.prevent()
    """
    def decoratePrevent(func):
        def preventFunction(*args, **kargs):
            val = False
            for arg in args:
                if extension.prevent(arg):
                    val = True
                    break

            if val:
                print "Not calling"
            else:
                ret = func(*args, **kargs)
                return ret

        return preventFunction
    return decoratePrevent

@prevent()
@ratelimit()
@dumpargs()
def post_folder_creation(src):
    options = { 'path': src }
    requests.post(ENDPOINTS['folder_create'], params=options)

@prevent()
@ratelimit()
@dumpargs()
def post_file_creation(src):
    options = { 'path': src }
    requests.post(ENDPOINTS['file_create'], params=options)

@prevent()
@ratelimit()
@dumpargs()
def post_folder_destroy(src):
    options = { 'path': src }
    requests.post(ENDPOINTS['folder_destroy'], params=options)

@prevent()
@ratelimit()
@dumpargs()
def post_file_destroy(src):
    options = { 'path': src }
    requests.post(ENDPOINTS['file_destroy'], params=options)

@prevent()
@ratelimit()
@dumpargs()
def post_folder_move(src, dest):
    options = { 'oldpath': src, 'newpath': dest }
    requests.post(ENDPOINTS['folder_move'], params=options)

@prevent()
@ratelimit()
@dumpargs()
def post_file_move(src, dest):
    options = { 'oldpath': src, 'newpath': dest }
    requests.post(ENDPOINTS['file_move'], params=options)
