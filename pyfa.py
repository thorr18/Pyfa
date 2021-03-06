#!/usr/bin/env python
#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import sys
import re
import config

from optparse import OptionParser, BadOptionError, AmbiguousOptionError


class PassThroughOptionParser(OptionParser):
    """
    An unknown option pass-through implementation of OptionParser.

    OSX passes -psn_0_* argument, which is something that pyfa does not handle. See GH issue #423
    """
    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self,largs,rargs,values)
            except (BadOptionError,AmbiguousOptionError), e:
                largs.append(e.opt_str)

# Parse command line options
usage = "usage: %prog [--root]"
parser = PassThroughOptionParser(usage=usage)
parser.add_option("-r", "--root", action="store_true", dest="rootsavedata",
                  help="if you want pyfa to store its data in root folder, use this option", default=False)
parser.add_option("-w", "--wx28", action="store_true", dest="force28",
                  help="Force usage of wxPython 2.8", default=False)
parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Set logger to debug level.", default=False)

(options, args) = parser.parse_args()

if not hasattr(sys, 'frozen'):
    print "pyfa build:", config.version
    if sys.version_info < (2,6) or sys.version_info >= (3,0):
        print("Pyfa requires python 2.x branch ( >= 2.6 )\nExiting.")
        sys.exit(1)
    else:
        print "platform version:", sys.version

    try:
        import wxversion
    except ImportError as er:
        print er.message  # wxversion is not included with all wx builds, but that's OK

    try:
        if options.force28 is True:
            wxversion.select('2.8')
        else:
            wxversion.select(['3.0', '2.8'])
    except (wxversion.VersionError, NameError) as er:
        print er.message  # wxversion is not very smart, so we will not give up yet

    try:
        import wx
        if 'phoenix' not in wx.PlatformInfo:
            print "wx version:", wx.version()
        else:
            raise ImportError("wx module must be 'classic'")
    except ImportError as er:
        print er.message
        print "wxPython doesn't meet requirements.\nInstall wxPython (2.8+) from http://www.wxpython.org/"
        sys.exit(1)

    try:
        import sqlalchemy

        saVersion = sqlalchemy.__version__
        saMatch = re.match("([0-9]+).([0-9]+)([b\.])([0-9]+)", saVersion)
        if saMatch:
            saMajor = int(saMatch.group(1))
            saMinor = int(saMatch.group(2))
            betaFlag = True if saMatch.group(3) == "b" else False
            saBuild = int(saMatch.group(4)) if not betaFlag else 0
            if saMajor == 0 and (saMinor < 5 or (saMinor == 5 and saBuild < 8)):
                print("Pyfa requires sqlalchemy 0.5.8 at least  but current sqlalchemy version is %s\n"
                      "You can download sqlalchemy (0.5.8+) from http://www.sqlalchemy.org/".format(saVersion))
                sys.exit(1)
        else:
            print("Unknown sqlalchemy version string format, skipping check")
            print saVersion

    except ImportError as er:
        print er.message
        print("You can download sqlalchemy (0.6+) from http://www.sqlalchemy.org/")
        sys.exit(1)
    
    # check also for dateutil module installed.
    try:
        import dateutil.parser  # Copied import statement from service/update.py
    except ImportError as er:
        print er.message
        print("You can download python-dateutil from https://pypi.python.org/pypi/python-dateutil")
        sys.exit(1)


def main():
    # Configure paths
    if options.rootsavedata is True:
        config.saveInRoot = True

    config.debug = options.debug
    config.defPaths()

    # Basic logging initialization
    import logging
    logging.basicConfig()

    # Import everything
    import os

    import eos.db
    import service.prefetch
    from gui.mainFrame import MainFrame

    #Make sure the saveddata db exists
    if not os.path.exists(config.savePath):
        os.mkdir(config.savePath)

    eos.db.saveddata_meta.create_all()

    pyfa = wx.App(False)
    MainFrame()
    pyfa.MainLoop()

if __name__ == '__main__':
    main()
print "loaded pyfa module"
