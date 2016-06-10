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
        src = event.src_path
        if self.is_hidden(src):
            # Events with hidden paths (dot files) are not registered
            return

        try:
            if event.is_directory:
                print "Created folder {0}".format(src)
                FileWatch.queue.enqueue(
                    'watchman.pigeon.post_folder_creation',
                    src
                )
            else:
                print "Created file {0}".format(src)
                FileWatch.queue.enqueue(
                    'watchman.pigeon.post_file_creation',
                    src
                )
        except Exception, e:
            print(e)

    def on_deleted(self, event):
        src = event.src_path
        if self.is_hidden(src):
            # Events with hidden paths (dot files) are not registered
            return

        try:
            if event.is_directory:
                print "Deleted folder {0}".format(src)
                FileWatch.queue.enqueue(
                    'watchman.pigeon.post_folder_destroy',
                    src
                )
            else:
                print "Deleted file {0}".format(src)
                FileWatch.queue.enqueue(
                    'watchman.pigeon.post_file_destroy',
                    src
                )

        except Exception, e:
            print(e)

    def on_moved(self, event):
        src = event.src_path
        dest = event.dest_path
        if self.is_hidden(src) or self.is_hidden(dest):
            # Events with hidden paths (dot files) are not registered
            return

        try:
            if event.is_directory:
                print "Moved folder from {0} to {1}".format(src, dest)
                FileWatch.queue.enqueue(
                    'watchman.pigeon.post_folder_move',
                    src,
                    dest
                )
            else:
                print "Moved file from {0} to {1}".format(src, dest)
                FileWatch.queue.enqueue(
                    'watchman.pigeon.post_file_move',
                    src,
                    dest
                )
        except Exception, e:
            print(e)

    def is_hidden(self, path):
        m = re.search('(?<=\/\.)\w+', path)
        return m is not None
