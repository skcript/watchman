# -*- encoding: utf-8 -*-
import os
import time
import yaml
import logging
import subprocess
from watch import FileWatch
from threading import Thread
from watchman.conf import CONFIG_FILE, LOG_FILENAME, HREGEX, NREGEX, load_config

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
log = logging.getLogger("watchman.init")


class Watchman():
    filesync = None

    @staticmethod
    def configure():
        config = load_config(CONFIG_FILE)

        try:
            if len(config['source']) == 0:
                Watchman.get_source(config)

            yaml.dump(config, open(CONFIG_FILE, "w"), default_flow_style=False)

            log.info("Config written in %s" % CONFIG_FILE)
        except KeyboardInterrupt:
            log.error("Config cancelled by user")

    @staticmethod
    def get_source(config):
        source = raw_input("What is the source path?: ")
        if os.path.exists(source):
            print("Adding ({0})...".format(source))
            config['source'].append(source)
        else:
            print("Path does not exist!")
            Watchman.get_source(config)

        ans = raw_input("Add more paths? (y/n): ")
        if ans in {"y", "Y"}:
            Watchman.get_source(config)

    @staticmethod
    def sync():
        if not Watchman.filesync:
            Watchman.filesync = "Syncing..."
            print(Watchman.filesync)
            sync = Thread(target=Watchman.watch())
            sync.daemon = True
            sync.start()

    @staticmethod
    def watch():
        config = load_config(CONFIG_FILE)
        # Watchman.filesync = FileWatch(regexes = [NREGEX])
        Watchman.filesync = FileWatch()
        Watchman.filesync.start(config)

    @staticmethod
    def stop():
        print("Stopping...")
        Watchman.filesync.stop()
        Watchman.filesync = None
