# -*- encoding: utf-8 -*-
import os
import re
import yaml
import redis
import logging
import subprocess

LOG_FILENAME = 'watchman.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
log = logging.getLogger("watchman.conf")

CONFIG_FILE = os.path.expanduser("~/watchman.yml")

HREGEX = r"[^.]*"
NREGEX = r"([a-zA-Z0-9_ -/]*)/active/home/(\w+)/uploads/(\d+)/hot_root/"

def load_config(config_file=CONFIG_FILE):
    """ Try to load YAML config file. """
    config = {'source': []}
    if os.path.isfile(config_file):
        log.debug("Try loading config file: {0}".format(config_file))
        config = yaml.load(open(CONFIG_FILE)) or config
    else:
        log.debug("Try creating config file: {0}".format(config_file))
        open(config_file, 'w')

    return config
