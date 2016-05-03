# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2011-12-11.
#=============================================================================
#   observer_linux.py --- Observe creation of directories and files
#=============================================================================
import atexit
import os

import inotifyx

import base


class Observer(base.Observer):
    _fd = inotifyx.init()
    _wd = dict()

    @classmethod
    def add_observer(self, observer):
        self._observers.append(observer)
        observer._wd = inotifyx.add_watch(
            self._fd, observer.dir,
            inotifyx.IN_CREATE|inotifyx.IN_MOVE|inotifyx.IN_DELETE|inotifyx.IN_ATTRIB,
        )
        self._wd[observer._wd] = observer
    
    @classmethod
    def remove_observer(self, observer):
        inotifyx.rm_watch(self._fd, observer._wd)
        self._observers.remove(observer)
        del self._wd[observer._wd]
    
    @classmethod
    def check(self):
        for event in inotifyx.get_events(self._fd):
            self.log.debug('%s %r [%s]', event, event.name, event.cookie)
            if event.wd in self._wd:
                self._wd[event.wd].dispatch()
    
    @classmethod
    def close(self):
        os.close(self._fd)

atexit.register(Observer.close)

#.............................................................................
#   observer_linux.py
