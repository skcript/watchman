# -*- encoding: utf-8 -*-
import re
import time
import requests
import logging
from rratelimit import Limiter

# Modules in Watchman
from conf import load_endpoints, LOG_FILENAME, REDIS, RL_LIMIT, RL_PERIOD

ENDPOINTS = load_endpoints()
LIMITER = Limiter(REDIS, action='pigeon', limit=RL_LIMIT, period=RL_PERIOD)
REGEX = re.compile("([a-zA-Z0-9_ -/]*)/active/home/(\w+)/uploads/(\d+)/hot_root/")

# Logger Creds
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
log = logging.getLogger("watchman.pigeon")

def ratelimit():
    def decorate(func):
        def rateLimitedFunction(*args,**kargs):
            name = get_user_name(args[0])
            if name:
                while not LIMITER.checked_insert(name):
                    print "{0} is being rate limited".format(name)
                    time.sleep(0.05)
            else:
                print "Invalid args, {0}".format(args)

            ret = func(*args,**kargs)
            return ret

        return rateLimitedFunction
    return decorate

def get_user_name(path):
    r = REGEX.match(path)
    if r:
        name = r.group(2)
        return name

def check_path_processing(path):
    avl = REDIS.scan_iter(match="{0}*".format(path))
    return (sum(1 for _ in avl) > 0 or REDIS.get("migration") or REDIS.get("import") or REDIS.get("snapshot"))

@ratelimit()
def post_folder_creation(src):
    if check_path_processing(src):
        log.debug("Not sending folder creation for {0}".format(src))
        print("Not sending folder creation for {0}".format(src))
    else:
        log.debug("Sending folder creation for {0}".format(src))
        print("Sending folder creation for {0}".format(src))
        options = { 'path': src }
        requests.post(ENDPOINTS['folder_create'], params=options)

@ratelimit()
def post_file_creation(src):
    if check_path_processing(src):
        log.debug("Not sending file creation for {0}".format(src))
        print("Not sending file creation for {0}".format(src))
    else:
        log.debug("Sending file creation for {0}".format(src))
        print("Sending file creation for {0}".format(src))
        options = { 'path': src }
        requests.post(ENDPOINTS['file_create'], params=options)

@ratelimit()
def post_folder_destroy(src):
    log.debug("Removing folder at {0}".format(src))
    print("Removing folder at {0}".format(src))

    options = { 'path': src }
    requests.post(ENDPOINTS['folder_destroy'], params=options)

@ratelimit()
def post_file_destroy(src):
    log.debug("Removing file at {0}".format(src))
    print("Removing file at {0}".format(src))

    options = { 'path': src }
    requests.post(ENDPOINTS['file_destroy'], params=options)

@ratelimit()
def post_folder_move(src, dest):
    if check_path_processing(src) or check_path_processing(dest):
        log.debug("Not sending folder movement from {0} to {1}".format(src, dest))
        print("Not sending folder movement from {0} to {1}".format(src, dest))
    else:
        log.debug("Sending folder movement from {0} to {1}".format(src, dest))
        print("Sending folder movement from {0} to {1}".format(src, dest))
        options = { 'oldpath': src, 'newpath': dest }
        requests.post(ENDPOINTS['folder_move'], params=options)

@ratelimit()
def post_file_move(src, dest):
    if check_path_processing(src) or check_path_processing(dest):
        log.debug("Not sending file movement from {0} to {1}".format(src, dest))
        print("Not sending file movement from {0} to {1}".format(src, dest))
    else:
        log.debug("Sending file movement from {0} to {1}".format(src, dest))
        print("Sending file movement from {0} to {1}".format(src, dest))
        options = { 'oldpath': src, 'newpath': dest }
        requests.post(ENDPOINTS['file_move'], params=options)
