# -*- encoding: utf-8 -*-
import os
import re
import yaml
import redis
import logging

# Log configs
LOG_FILENAME = 'watchman.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
log = logging.getLogger("watchman.conf")

# Queuing system configs
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
QUEUES = ['default', 'filewatcher', 'reports']

# Settings file
CONFIG_FILE = os.path.expanduser("~/watchman.yml")

def load_paths():
    """ Try to load paths. """
    if not os.path.isfile(CONFIG_FILE):
        return []

    paths = yaml.load(open(CONFIG_FILE))['source']
    if isinstance(paths, list):
        return paths
    else:
        return []

def load_regexes():
    """ Try to load regexes. """
    if not os.path.isfile(CONFIG_FILE):
        return []

    regexes = yaml.load(open(CONFIG_FILE))['regexes']
    if isinstance(regexes, list):
        return regexes
    else:
        return []

def load_endpoints():
    """ Try to load regexes. """
    if not os.path.isfile(CONFIG_FILE):
        return {}

    endpoints = yaml.load(open(CONFIG_FILE))['endpoints']
    if isinstance(endpoints, dict):
        return endpoints
    else:
        return {}

def load_config(config_file=CONFIG_FILE):
    """ Try to load YAML config file. """
    config = {'source': [], 'regexes': [], 'endpoints': {}}
    if os.path.isfile(config_file):
        log.debug("Try loading config file: {0}".format(config_file))
        config = yaml.load(open(config_file)) or config
    else:
        log.debug("Try creating config file: {0}".format(config_file))
        open(config_file, 'w')

    return config

def update_config(config, config_file=CONFIG_FILE):
    """ Try to update YAML config file. """
    yaml.dump(config, open(config_file, "w"), default_flow_style=False)
    log.info("Updated config in %s" % CONFIG_FILE)
