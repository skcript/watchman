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
from worker import work
import configurations

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
log = logging.getLogger("watchman.init")

class Watchman():
    @staticmethod
    def configure():
        config = load_config()

        try:
            while True:
                ans = raw_input("MENU \n 1. Add Source 2.Remove Source 3. View 4. Save \n")
                if (int(ans) == 1):
                    configurations.add_source(config)
                elif (int(ans) ==  2):
                    configurations.remove_source(config)
                elif (int(ans) == 3):
                    configurations.view_source(config)
                elif (int(ans) == 4):
                    update_config(config)
                else:
                    print "Huh? That wasn't even an option. -_-"
        except KeyboardInterrupt:
            log.error("Config cancelled by user")

    @staticmethod
    def sync():
        FileWatch(regexes = load_regexes()).start()

    @staticmethod
    def work():
        work()
