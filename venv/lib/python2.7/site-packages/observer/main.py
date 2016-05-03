# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2011-12-11.
#=============================================================================
#   main.py --- 
#=============================================================================
import logging
import os, signal

from autorestart import AutorestartObserver


def handle_term():
    def sighandler(signum, frame):
        os.kill(os.getpid(), signal.SIGINT)
    signal.signal(signal.SIGTERM, sighandler)

def main(args):
    logging.basicConfig()
    handle_term()
    root = AutorestartObserver('.', args)
    try:
        root.loop()
    except KeyboardInterrupt:
        root.kill_child()

#.............................................................................
#   main.py
