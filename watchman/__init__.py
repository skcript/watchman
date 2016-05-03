# -*- encoding: utf-8 -*-
import os
import time
import yaml
import logging
import subprocess
from watch import FileWatch
from threading import Thread

# Modules in Watchman
from conf import LOG_FILENAME, load_regexes, load_config, update_config

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
log = logging.getLogger("watchman.init")

class Watchman():
    @staticmethod
    def configure():
        config = load_config()

        try:
            if len(config['source']) == 0:
                Watchman.get_source(config)

            update_config(config)
        except KeyboardInterrupt:
            log.error("Config cancelled by user")

    @staticmethod
    def get_source(config):
        source = raw_input("What is the source path?: ")
        if os.path.exists(source):
            print("Adding ({0})...".format(source))
            config['source'].append(source)
            ans = raw_input("Add more paths? (y/n): ")
            if ans in {"y", "Y"}:
                Watchman.get_source(config)
        else:
            print("Path does not exist!")
            Watchman.get_source(config)

    @staticmethod
    def sync():
        FileWatch(regexes = load_regexes()).start()
