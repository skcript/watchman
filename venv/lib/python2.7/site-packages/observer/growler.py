# -*- coding:utf-8 -*-
# Created by Hans-Thomas on 2011-05-13.
#=============================================================================
#   growler.py --- Growl notifier
#=============================================================================
from os.path import abspath, dirname, join

from gntp.notifier import GrowlNotifier


class Notifier(object):
    
    def __init__(self, app_name='autorestart'):
        self.growl = GrowlNotifier(
            applicationName = app_name,
            notifications = ['New Message'],
            defaultNotifications = ['New Message']
        )
        self.growl.register()

    def notify(self, title, description, sticky=False):
        self.growl.notify(
            noteType = 'New Message',
            title = title,
            description = description,
            sticky = sticky,
        )

#.............................................................................
#   growler.py
