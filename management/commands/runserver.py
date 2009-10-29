#!/usr/bin/env python

"""
    Django command to run development server and keep CSS files up to date.
    The syntax is the same as Django's runserver command (in fact this is just
    a very light wrapper around said command). Passing --noreload also tells
    the CSS autoreloader not to run. When code is reloaded there is no need
    to restart the CSS autoreloader, so it is started only once at startup.
"""

import os
import tempfile
import threading
import time

from django.core.management.commands.runserver import Command as RunServer

from ccss import Command as Ccss


class Reloader(threading.Thread):
    """
        A thread based on the functionality in django.utils.autoreload. It
        basically polls every second for updated files and generates new
        CSS from any updated templates. It's very simple and has no
        dependencies other than Python.
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        # FIXME: remove the following when Django is fixed!
        # There is a bug in Django where autoreloading causes some weird
        # thread issues and this will be run multiple times. Let's make sure
        # we only actually execute the reloader once. We do this with a little
        # hack by writing our process id to a file, waiting, then reading it.
        # If the value read back is the same, then run, otherwise quit. This
        # lets the weird threads duke it out with only one surviving to
        # actually run.
        filename = os.path.join(os.path.dirname(__file__), ".pid")
        open(filename, "w").write(str(os.getpid()))

        time.sleep(0.5)

        pid = int(open(filename).read())
        if pid != os.getpid():
            return

        # Actual reloader
        print "Starting CleverCSS autoreloader..."
        cmd = Ccss()
        try:
            while True:
                cmd.handle(verbosity=1)
                time.sleep(1)
        except KeyboardInterrupt:
            pass


class Command(RunServer):
    """
        Wrap the built-in Django runserver command. This does the exact same
        thing except also launches the CSS reloader.
    """

    def handle(self, *args, **options):
        # Should we start the CSS reloader?
        if options.get('use_reloader', True):
            reload_thread = Reloader()
            reload_thread.start()

        # Invoke runserver command like normal
        super(Command, self).handle(*args, **options)
