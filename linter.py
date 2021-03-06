#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Jon Surrell
# Copyright (c) 2014 Jon Surrell
#
# License: MIT
#

"""This module exports the Gotype plugin class."""

from os.path import dirname
from SublimeLinter.lint import Linter, util


class Gotype(Linter):
    """Provides an interface to gotype."""

    syntax = ('go', 'gosublime-go')
    executable = "gotype"
    regex = r'(?P<filename>^.+):(?P<line>\d+):(?P<col>\d+):\s+(?P<message>.+)'
    error_stream = util.STREAM_STDERR

    def __init__(self, view, syntax):
        """Initialize and load GOPATH from settings if present."""
        super(Gotype, self).__init__(view, syntax)

        gopath = self.get_view_settings().get('gopath')
        if gopath:
            if self.env:
                self.env['GOPATH'] = gopath
            else:
                self.env = {'GOPATH': gopath}

    def cmd(self):
        """Return the command line to run."""
        return [self.executable_path, "-e", "-a", dirname(self.filename)]

    def split_match(self, match):
        """Process each match modifying or discarding it."""
        match, line, col, error, warning, message, near = super().split_match(match)
        if match.group("filename") != self.filename:
            return None, None, None, None, None, '', None
        return match, line, col, error, warning, message, near
