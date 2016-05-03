# -*- encoding: utf-8 -*-
import requests
import logging

# Modules in Watchman
from conf import load_endpoints, LOG_FILENAME

ENDPOINTS = load_endpoints()

# Logger Creds
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
log = logging.getLogger("watchman.pigeon")

def post_folder_creation(src):
    log.debug("post_folder_creation")
    
    options = { 'path': src }
    requests.post(ENDPOINTS['folder_create'], params=options)

def post_file_creation(src):
    log.debug("post_file_creation")
    
    options = { 'path': src }
    requests.post(ENDPOINTS['file_create'], params=options)

def post_folder_destroy(src):
    log.debug("post_folder_destroy")
    
    options = { 'path': src }
    requests.post(ENDPOINTS['folder_destroy'], params=options)

def post_file_destroy(src):
    log.debug("post_file_destroy")
    
    options = { 'path': src }
    requests.post(ENDPOINTS['file_destroy'], params=options)

def post_folder_move(src, dest):
    log.debug("post_folder_move")
    
    options = { 'oldpath': src, 'newpath': dest }
    requests.post(ENDPOINTS['folder_move'], params=options)

def post_file_move(src, dest):
    log.debug("post_file_move")
    
    options = { 'oldpath': src, 'newpath': dest }
    requests.post(ENDPOINTS['file_move'], params=options)
