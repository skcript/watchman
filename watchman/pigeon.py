# -*- encoding: utf-8 -*-
import re
import time
import requests
import logging
from rratelimit import Limiter

# Modules in Watchman
from conf import load_endpoints, LOG_FILENAME, REDIS, RL_LIMIT, RL_PERIOD

ENDPOINTS = load_endpoints()
# Ratelimiter limiting pigeon at RL_LIMIT actions per RL_PERIOD
LIMITER = Limiter(REDIS, action='pigeon', limit=RL_LIMIT, period=RL_PERIOD)

# Logger Creds
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
log = logging.getLogger("watchman.pigeon")

# Regex to extract name from path watched
REGEX = re.compile("([a-zA-Z0-9_ -/]*)/active/home/(\w+)/")

# Extracting user name from path
def get_user_name(path):
    r = REGEX.match(path)
    if r:
        name = r.group(2)
        return name

# Checking if server is ready to accept request for that path
def check_paths(path):
    avl = REDIS.scan_iter(match="{0}*".format(path))
    srv = REDIS.get("migration") or REDIS.get("import") or REDIS.get("snapshot")
    return (sum(1 for _ in avl) > 0 or srv)

# Ratelimiting server pings at RL_LIMIT actions per RL_PERIOD
def ratelimit():
    def decorate(func):
        def rateLimitedFunction(*args,**kargs):
            name = get_user_name(args[0])
            if name:
                while not LIMITER.checked_insert(name):
                    print "{0} is being rate limited".format(name)
                    time.sleep(0.5)
            else:
                print "Invalid args, {0}".format(args)

            ret = func(*args,**kargs)
            return ret

        return rateLimitedFunction
    return decorate

def dumpargs():
    """
        This decorator dumps out the arguments passed to a function before
        calling it
    """
    def decorate(func):
        argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
        fname = func.func_name
        def decorateDump(*args, **kargs):
            string = "Calling '" + fname + "' with args: " + ", ".join(
                                            '%s=%r' % entry
                                            for entry in zip(argnames, args[:len(argnames)])
                                        )
            print string

            ret = func(*args, **kargs)
            return ret

        return decorateDump
    return decorate

def prevent():
    def decorate(func):
        def decorateDump(*args, **kargs):
            val = True
            for arg in args:
                if check_paths(arg):
                    val = False
                    break

            if val:
                ret = func(*args, **kargs)
                return ret
            else:
                print "Not calling"

        return decorateDump
    return decorate

@dumpargs()
@prevent()
@ratelimit()
def post_folder_creation(src):
    options = { 'path': src }
    requests.post(ENDPOINTS['folder_create'], params=options)

@dumpargs()
@prevent()
@ratelimit()
def post_file_creation(src):
    options = { 'path': src }
    requests.post(ENDPOINTS['file_create'], params=options)

@dumpargs()
@prevent()
@ratelimit()
def post_folder_destroy(src):
    options = { 'path': src }
    requests.post(ENDPOINTS['folder_destroy'], params=options)

@dumpargs()
@prevent()
@ratelimit()
def post_file_destroy(src):
    options = { 'path': src }
    requests.post(ENDPOINTS['file_destroy'], params=options)

@dumpargs()
@prevent()
@ratelimit()
def post_folder_move(src, dest):
    options = { 'oldpath': src, 'newpath': dest }
    requests.post(ENDPOINTS['folder_move'], params=options)

@dumpargs()
@prevent()
@ratelimit()
def post_file_move(src, dest):
    options = { 'oldpath': src, 'newpath': dest }
    requests.post(ENDPOINTS['file_move'], params=options)
