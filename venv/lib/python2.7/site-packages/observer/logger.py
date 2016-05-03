# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2011-05-11.
#=============================================================================
#   logger.py --- Logger meta class
#=============================================================================
import logging


class MetaLogger(type):

    def __new__(self, classname, bases, classdict):
        classdict.setdefault('log', logging.getLogger('%s.%s' % (classdict['__module__'], classname)))
        return type.__new__(self, classname, bases, classdict)

class Logger(object):
    __metaclass__ = MetaLogger

#.............................................................................
#   logger.py
