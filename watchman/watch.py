# -*- encoding: utf-8 -*-
import os
import re
import time
import shutil
import requests

from rq import Queue
from redis import Redis
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

# Modules in Watchman
import watchman.pigeon
from conf import load_paths, REDIS

class FileWatch(RegexMatchingEventHandler):
    queue = Queue('filewatcher', connection=REDIS)

    def start(self):
        self.ignore_files = [".DS_Store", "desktop.ini"]

        self.observer = Observer()
        for path in load_paths():
            print path
            self.observer.schedule(self, path=path, recursive=True)
        self.observer.start()
        print "* Running Watchman (Press CTRL+C to quit)"

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def stop(self):
        self.observer.stop()

    def on_created(self, event):
        try:
            src = event.src_path

            if event.is_directory:
                print "Created folder {0}".format(src)
                FileWatch.queue.enqueue('watchman.pigeon.post_folder_creation', src)
            elif not os.path.basename(event.src_path) in self.ignore_files:
                print "Created file {0}".format(src)
                FileWatch.queue.enqueue('watchman.pigeon.post_file_creation', src)
        except Exception, e:
            print(e)

    def on_deleted(self, event):
        try:
            src = event.src_path

            if event.is_directory:
                print "Deleted folder {0}".format(src)
                FileWatch.queue.enqueue('watchman.pigeon.post_folder_destroy', src)
            elif not os.path.basename(event.src_path) in self.ignore_files:
                print "Deleted file {0}".format(src)
                FileWatch.queue.enqueue('watchman.pigeon.post_file_destroy', src)

        except Exception, e:
            print(e)

    def on_moved(self, event):
        try:
            src = event.src_path
            dest = event.dest_path

            if event.is_directory:
                print "Moved folder from {0} to {1}".format(src, dest)
                FileWatch.queue.enqueue('watchman.pigeon.post_folder_move', src, dest)
            elif not os.path.basename(event.src_path) in self.ignore_files:
                print "Moved file from {0} to {1}".format(src, dest)
                FileWatch.queue.enqueue('watchman.pigeon.post_file_move', src, dest)
        except Exception, e:
            print(e)

    def on_modified(self, event):
        try:
            src = event.src_path

            if event.is_directory:
                print "Modified folder {0}".format(src)
            elif not os.path.basename(event.src_path) in self.ignore_files:
                print "Modified file {0}".format(src)
        except Exception, e:
            print(e)
