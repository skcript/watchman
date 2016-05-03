# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2011-12-11.
#=============================================================================
#   observer.py --- Observe creation of directories and files
#=============================================================================
import glob
import hashlib
import os.path
import time

from logger import Logger


class Observer(Logger):    
    _observers = []
    
    @classmethod
    def add_observer(self, observer):
        self._observers.append(observer)
    
    @classmethod
    def remove_observer(self, observer):
        self._observers.remove(observer)
    
    @classmethod
    def check(self):
        for observer in self._observers:
            observer.dispatch()
    
    @classmethod
    def loop(self, interval=1):
        while True:
            self.check()
            time.sleep(interval)
    
    def __init__(self, dir, pattern, changes=False, dirs=False):
        self.dir = dir
        self.pattern = pattern
        self.entries = set()
        self._changes = changes
        if dirs:
            self._check_type = os.path.isdir
        else:
            self._check_type = os.path.isfile
        self.update()
        for entry in self.entries:
            self.on_create(os.path.basename(entry))
    
    def _basename(self, path):
        return path[len(self.dir) + 1:]
    
    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.dir, self.pattern)
    
    def changes(self):
        entries = self.entries
        self.update()
        return (
            sorted(map(self._basename, self.entries - entries)),
            sorted(map(self._basename, self.file_changes())),
            sorted(map(self._basename, entries - self.entries))
        )
    
    def file_changes(self):
        if self._changes:
            checksums = self.checksums
            self.update_file_changes()
            for key in self.entries:
                if key in checksums and checksums[key] != self.checksums[key]:
                    yield key
    
    def check_entry(self, entry):
        return self._check_type(entry)
    
    def update(self):
        self.entries = set(f for f in glob.glob(os.path.join(self.dir, self.pattern)) if self.check_entry(f))
        self.log.debug('update:entries:%s', self.entries)
    
    def update_file_changes(self):
        self.checksums = dict((key, file_sha1(key).digest()) for key in self.entries)
    
    def dispatch(self):
        created, changed, deleted = self.changes()
        for entry in created:
            self.on_create(entry)
        for entry in changed:
            self.on_change(entry)
        for entry in deleted:
            self.on_delete(entry)
    
    def on_create(self, entry):
        self.log.debug('%s.on_create:%s', self, entry)
    
    def on_change(self, entry):
        self.log.debug('%s.on_change:%s', self, entry)
    
    def on_delete(self, entry):
        self.log.debug('%s.on_delete:%s', self, entry)

def file_sha1(path):
    sha1 = hashlib.sha1()
    with open(path) as f:
        while True:
            data = f.read(4096)
            if not data:
                return sha1
            sha1.update(data)

#.............................................................................
#   observer.py
