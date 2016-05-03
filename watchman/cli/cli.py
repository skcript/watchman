# -*- encoding: utf-8 -*-
"""
Watchman command line tool
"""

import click

from watchman import Watchman

# Disable the warning that Click displays (as of Click version 5.0) when users
# use unicode_literals in Python 2.
# See http://click.pocoo.org/dev/python3/#unicode-literals for more details.
click.disable_unicode_literals_warning = True

@click.group()
def main():
    """Watchman command line tool."""
    pass

@main.command()
def sync():
    """Start watching sources."""
    Watchman.sync()

@main.command()
def worker():
    """Start watchman worker."""
    Watchman.work()

@main.command()
def configure():
    """Configure watchman."""
    Watchman.configure()
