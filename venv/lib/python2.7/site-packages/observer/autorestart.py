# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2011-12-11.
#=============================================================================
#   autorestart.py --- Restart program on file change
#=============================================================================
import logging
import os
import re
import signal
import subprocess
import threading

from observer.gitignore import GitIgnore
from observer.tree import TreeObserver


try:
    from growler import Notifier
except ImportError:
    growler = None
else:
    growler = Notifier()


log = logging.getLogger(__name__)

DEFAULT_FILEPATTERN = re.compile(r'.*\.(py|txt|yaml|sql|html|js|css)$')

class AutorestartObserver(TreeObserver):
    
    def __init__(self, dir, args, filepattern=DEFAULT_FILEPATTERN):
        self._lock = threading.Lock()
        self.child = None
        self.args = args
        super(AutorestartObserver, self).__init__(dir, filepattern, GitIgnore(dir))
    
    @property
    def child(self):
        with self._lock:
            return self._child
    
    @child.setter
    def child(self, child):
        with self._lock:
            self._child = child
    
    def kill_child(self):
        child = self.child
        if child is not None:
            child.terminate()
            child.wait()
            self.child = None
    
    def restart_child(self):
        self.kill_child()
        self.child = subprocess.Popen(self.args, close_fds=True)
    
    def action(self, entries):
        restarted = self.child is not None
        self.restart_child()
        if growler is not None:
            growler.notify(
                '{}started: {}'.format('re' if restarted else '',
                ' '.join(self.args)), 'in {}'.format(os.getcwd()),
            )

#.............................................................................
#   autorestart.py
