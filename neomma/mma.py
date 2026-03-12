#!/usr/bin/python3

"""
The program "MMA - Musical Midi Accompaniment" and the associated
modules distributed with it are protected by copyright.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

Bob van der Poel <bob@mellowood.ca>

"""

import sys
import os
import platform

MMAdir = os.path.dirname(__file__)

def main():
    # Ensure a proper version is available.
    # This test forces 2.6+ or 3.x
    if sys.version_info[0] == 2 and sys.version_info[1] < 6:
        print ("\nYou need a more current version of Python to run MMA.")
        print ("We're looking for something equal or greater than version 2.6")
        print ("Current Python version is %s\n" % sys.version)
        sys.exit(0)

    from .MMA import main as mmaMain    # this runs the program

if __name__ == "__main__":
    main()