# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2011-12-22.
#=============================================================================
#   gitignore.py --- 
#=============================================================================
"""
>>> matcher = GitIgnore(os.path.abspath(os.getcwd()))

>>> matcher('observer.egg-info')
True

>>> matcher('./observer.egg-info')
True

>>> matcher('.gitignore')
False

>>> matcher('.DS_Store')
False

>>> matcher('observer/gitignore.pyc')
True

>>> matcher('.autocheck.db')
True
"""
import glob
import os

from logger import Logger


class GitIgnore(Logger):
    
    def __init__(self, root):
        self.root = os.path.abspath(root)
        self._matchers = dict()

    def _match(self, dir, path):
        self.log.debug('_match:[%s][%s]', dir, path)
        try:
            matchers = self._matchers[dir]
        except KeyError:
            matchers = self._matchers[dir] = self._make_matchers(dir)
        for matcher in matchers:
            if matcher(path):
                return True
        return False
    
    def _make_matchers(self, dir, gitignore=None):
        path = os.path.abspath(dir)
        if gitignore is None:
            gitignore = os.path.join(path, '.gitignore')
        if not os.path.exists(gitignore):
            matchers = tuple()
        else:
            matchers = tuple(self._make_matchers_from_file(path, gitignore))
        if path == self.root:
            exclude = os.path.join(path, '.git', 'info', 'exclude')
            if os.path.exists(exclude):
                matchers += tuple(self._make_matchers_from_file(path, exclude))
        return matchers
    
    def _make_matchers_from_file(self, dir, gitignore):
        for line in open(gitignore):
            line = line.strip()
            if line.startswith('#'):
                continue
            if not line:
                continue
            self.log.debug('%s: %s', gitignore, line)
            yield self._make_matcher_from_line(dir, line)
    
    def _make_matcher_from_line(self, dir, line):
            if line.endswith('/'):
                line = line.rstrip('/')
                checkdir = os.path.isdir
            else:
                def checkdir(path):
                    return True
            if line.startswith('/'):
                line = line.lstrip('/')
                def makepattern(fullpath):
                    return os.path.join(dir, line)
            else:
                def makepattern(fullpath):
                    return os.path.join(os.path.dirname(fullpath), line)
            def matcher(path):
                fullpath = os.path.join(dir, path)
                if not checkdir(fullpath):
                    return False
                pattern = makepattern(fullpath)
                self.log.debug('globbing: %r', pattern)
                globs = glob.glob(pattern)
                self.log.debug('globs: %s', globs)
                return fullpath in globs
            return matcher
    
    def __call__(self, path):
        dir = os.path.abspath(os.path.dirname(path))
        path = os.path.basename(path)
        while dir != self.root:
            if self._match(dir, path):
                return True
            path = os.path.join(os.path.basename(dir), path)
            dir = os.path.dirname(dir)
        if self._match(self.root, path):
            return True
        return False

#.............................................................................
#   gitignore.py
