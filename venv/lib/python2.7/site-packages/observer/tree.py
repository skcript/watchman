# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2011-12-11.
#=============================================================================
#   tree.py --- Tree observer
#=============================================================================
import os
import threading
from Queue import Queue

from logger import Logger
from observer import Observer


class FileObserver(Observer):

    def __init__(self, dir, filepattern, queue):
        self.filepattern = filepattern
        self.queue = queue
        super(FileObserver, self).__init__(dir, '*', changes=True)
        self.update_file_changes()

    def check_entry(self, entry):
        return self.filepattern.match(entry)

    def enqueue(self, entry):
        self.queue.put(os.path.join(self.dir, entry))

    def on_create(self, entry):
        self.log.debug('on_create: "%s"', entry)
        self.enqueue(entry)

    def on_change(self, entry):
        self.log.debug('on_change: "%s"', entry)
        self.enqueue(entry)

    def on_delete(self, entry):
        self.log.debug('on_delete: "%s"', entry)
        self.enqueue(entry)


class DirObserver(Observer):

    def __init__(self, dir, filepattern, ignore, queue):
        self.observers = dict()
        self.filepattern = filepattern
        self.ignore = ignore
        self.queue = queue
        super(DirObserver, self).__init__(dir, '*')
        observer = FileObserver(dir, filepattern, queue)
        self.add_observer(observer)
        self.observers[None] = observer

    def __del__(self):
        for observer in self.observers.values():
            self.remove_observer(observer)

    def check_entry(self, entry):
        if os.path.isdir(entry):
             return self.ignore is None or not self.ignore(entry)

    def on_create(self, entry):
        self.log.debug('on_create: "%s"', entry)
        observer = DirObserver(os.path.join(self.dir, entry), self.filepattern, self.ignore, self.queue)
        self.add_observer(observer)
        self.observers[entry] = observer

    def on_delete(self, entry):
        self.log.debug('on_delete: "%s"', entry)
        if entry in self.observers:
            self.remove_observer(self.observers.pop(entry))


class TreeObserver(threading.Thread, Logger):
    
    def __init__(self, basedir, filepattern, ignore):
        super(TreeObserver, self).__init__()
        self.queue = Queue()
        self.root = DirObserver(basedir, filepattern, ignore, self.queue)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            entries = [self.queue.get()]
            while not self.queue.empty():
                entries.append(self.queue.get_nowait())
            self.log.debug('entries %s', entries)
            self.action(entries)

    def loop(self, interval=1):
        self.root.loop(interval)

    def action(self, entries):
        self.log.warn('TreeObserver:action: not implemented')


#.............................................................................
#   tree.py
