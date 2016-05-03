# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2011-12-11.
#=============================================================================
#   observer_macosx.py --- Observe creation of directories and files
#=============================================================================
import os

import kqueue

import base


class Observer(base.Observer):
    _kqueue = kqueue.kqueue()
    _ident = dict()

    @classmethod
    def add_observer(self, observer):
        self._observers.append(observer)
        observer._kevent = kqueue.EV_SET(
            os.open(observer.dir, os.O_RDONLY),
            kqueue.EVFILT_VNODE, kqueue.EV_ADD|kqueue.EV_CLEAR,
            kqueue.NOTE_RENAME|kqueue.NOTE_WRITE|kqueue.NOTE_DELETE|kqueue.NOTE_ATTRIB
        )
        self._ident[observer._kevent.ident] = observer
    
    @classmethod
    def remove_observer(self, observer):
        kqueue.EV_SET(observer._kevent.ident, kqueue.EVFILT_VNODE, kqueue.EV_DELETE)
        self._observers.remove(observer)
        del self._ident[observer._kevent.ident]
        observer.close()
    
    @classmethod
    def check(self):
        for kevent in self._kqueue.kevent([o._kevent for o in self._ident.itervalues()], 10, None):
            self.log.debug('%r', kevent)
            self._ident[kevent.ident].dispatch()

    def __delete__(self):
        self.close()
    
    def close(self):
        os.close(self._kevent.ident)

#.............................................................................
#   observer_macosx.py
