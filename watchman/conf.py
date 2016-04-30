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

REGEX_FILE = "regexes.yml"
CONFIG_FILE = os.path.expanduser("~/watchman.yml")

def load_regexes():
    if os.path.isfile(REGEX_FILE):
        return []

    regexes = yaml.load(open(REGEX_FILE))
    if isinstance(regexes, list):
        return []
    else:
        return regexes


def load_config(config_file=CONFIG_FILE):
    """ Try to load YAML config file. """
    config = {'source': []}
    if os.path.isfile(config_file):
        log.debug("Try loading config file: {0}".format(config_file))
        config = yaml.load(open(config_file)) or config
    else:
        log.debug("Try creating config file: {0}".format(config_file))
        open(config_file, 'w')

    return config

def update_config(config, config_file=CONFIG_FILE):
    yaml.dump(config, open(config_file, "w"), default_flow_style=False)
    log.info("Updated config in %s" % CONFIG_FILE)
