# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2011-12-11.
#=============================================================================
#   __init__.py --- Observe creation of directories and files
#=============================================================================
try:
    from observer_linux import Observer
except ImportError:
    try:
        from observer_macosx import Observer
    except ImportError:
        from observer.base import Observer

#.............................................................................
#   __init__.py
