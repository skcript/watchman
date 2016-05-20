# -*- encoding: utf-8 -*-
import requests
import logging

# Modules in Watchman
from conf import load_endpoints, LOG_FILENAME, REDIS

ENDPOINTS = load_endpoints()

# Logger Creds
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
log = logging.getLogger("watchman.pigeon")

def check_path_processing(path):
    avl = REDIS.scan_iter(match="{0}*".format(path))
    return (sum(1 for _ in avl) > 0 or REDIS.get("migration") or REDIS.get("import") or REDIS.get("snapshot"))

def post_folder_creation(src):
    if check_path_processing(src):
        log.debug("Not sending folder creation for {0}".format(src))
    else:
        log.debug("Sending folder creation for {0}".format(src))
        options = { 'path': src }
        requests.post(ENDPOINTS['folder_create'], params=options)

def post_file_creation(src):
    if check_path_processing(src):
        log.debug("Not sending file creation for {0}".format(src))
    else:
        log.debug("Sending file creation for {0}".format(src))
        options = { 'path': src }
        requests.post(ENDPOINTS['file_create'], params=options)

def post_folder_destroy(src):
    log.debug("Removing folder at {0}".format(src))

    options = { 'path': src }
    requests.post(ENDPOINTS['folder_destroy'], params=options)

def post_file_destroy(src):
    log.debug("Removing file at {0}".format(src))

    options = { 'path': src }
    requests.post(ENDPOINTS['file_destroy'], params=options)

def post_folder_move(src, dest):
    if check_path_processing(src) or check_path_processing(dest):
        log.debug("Not sending folder movement from {0} to {1}".format(src, dest))
    else:
        log.debug("Sending folder movement from {0} to {1}".format(src, dest))
        options = { 'oldpath': src, 'newpath': dest }
        requests.post(ENDPOINTS['folder_move'], params=options)

def post_file_move(src, dest):
    if check_path_processing(src) or check_path_processing(dest):
        print("Not sending file movement")
        log.debug("Not sending file movement from {0} to {1}".format(src, dest))
    else:
        log.debug("Sending file movement from {0} to {1}".format(src, dest))
        options = { 'oldpath': src, 'newpath': dest }
        requests.post(ENDPOINTS['file_move'], params=options)
