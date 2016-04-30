# -*- encoding: utf-8 -*-
import os
import re
import time
import shutil
import requests

from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

from watchman.conf import load_endpoints, load_paths

class FileWatch(RegexMatchingEventHandler):
    def start(self):
        self.paths = load_paths()
        self.endpoints = load_endpoints()
        self.ignore_files = [".DS_Store", "desktop.ini"]

        self.observer = Observer()
        for path in self.paths:
            print path
            self.observer.schedule(self, path=path, recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def on_created(self, event):
        try:
            src = event.src_path
            options = { 'path': src }

            if event.is_directory:
                print "Created folder {0}".format(src)
                requests.post(self.endpoints['folder_create'], params=options)
            elif not os.path.basename(event.src_path) in self.ignore_files:
                print "Created file {0}".format(src)
                requests.post(self.endpoints['file_create'], params=options)
        except Exception, e:
            print(e)

    def on_deleted(self, event):
        try:
            src = event.src_path
            options = { 'path': src }

            if event.is_directory:
                print "Deleted folder {0}".format(src)
                requests.post(self.endpoints['folder_destroy'], params=options)
            elif not os.path.basename(event.src_path) in self.ignore_files:
                print "Deleted file {0}".format(src)
                requests.post(self.endpoints['file_destroy'], params=options)

        except Exception, e:
            print(e)

    def on_moved(self, event):
        try:
            src = event.src_path
            dest = event.dest_path

            options = { 'oldpath': src, 'newpath': dest }

            if event.is_directory:
                print "Moved folder from {0} to {1}".format(src, dest)
                requests.post(self.endpoints['folder_move'], params=options)
            elif not os.path.basename(event.src_path) in self.ignore_files:
                print "Moved file from {0} to {1}".format(src, dest)
                requests.post(self.endpoints['file_move'], params=options)
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
