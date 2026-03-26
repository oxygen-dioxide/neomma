# main.py

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

import os

import neomma.MMA.midi
import neomma.MMA.midifuncs
import neomma.MMA.parse
import neomma.MMA.file
import neomma.MMA.options
import neomma.MMA.auto
import neomma.MMA.docs
import neomma.MMA.tempo
import neomma.MMA.debug
import neomma.MMA.paths
import neomma.MMA.writeMid

from neomma.MMA.safe_eval import safeEnv

from . import gbl
from neomma.MMA.common import *


cmdSMF = None

########################################
########################################

# This is the program mainline. It is called/executed
# exactly once from a call in the stub program mma.py.

# for some reason, someone might want a different encoding
# real easy to set it from env at startup
m = safeEnv("MMA_ENCODING")
if m:  # don't set to empty ... will crash
    gbl.encoding = m

# MMA prints errors/warning/debug to stdout
# this will redirect to a file
gbl.logFile = safeEnv("MMA_LOGFILE")

neomma.MMA.paths.init()  # initialize the lib/include paths

# Parse command line with click

neomma.MMA.options.cli(standalone_mode=False)


#  LibPath and IncPath are set before option parsing, but
#  debug setting wasn't. So we need to do the debug for this now
if neomma.MMA.debug.debug:
    dPrint("Initialization has set LibPath set to %s" % neomma.MMA.paths.libPath)
    dPrint("Initialization has set IncPath set to %s" % neomma.MMA.paths.incPath)

#######################################
# Set up initial meta track stuff. Track 0 == meta

m = gbl.mtrks[0] = neomma.MMA.midi.Mtrk(0)

if gbl.infile:
    if gbl.infile != 1:
        fileName = neomma.MMA.file.locFile(gbl.infile, None)
        if fileName and not gbl.noCredit:
            m.addTrkName(0, "%s" % fileName.rstrip(".mma"))
            m.addText(0, "Created by neomma.")


m.addTempo(0, gbl.tempo)  # most user files will override this
neomma.MMA.tempo.setTime(["4/4"])  # and this. IMPORTANT! Sets default chordTabs[]

# Read RC files
neomma.MMA.paths.readRC()


################################################
# Update the library database file(s) (-g option)
# Note: This needs to be here, after reading of RC files

if gbl.makeGrvDefs:
    if gbl.infile:
        error("No filename is permitted with the -g option")
    neomma.MMA.auto.libUpdate()  # update and EXIT


################################
# We need an input file for anything after this point.

if not gbl.infile:
    if gbl.createDocs:
        gbl.lineno = -1
        error("--doc options require a filename.")
    error("No input filename specified.")

################################
# Just extract docs (-Dxh, etc) to stdout.

if gbl.createDocs:
    if gbl.createDocs == 4:
        neomma.MMA.docs.htmlGraph(gbl.infile)
    else:
        f = neomma.MMA.file.locFile(gbl.infile, None)
        if not f:
            error("File '%s' not found" % gbl.infile)
        neomma.MMA.parse.parseFile(f)
        neomma.MMA.docs.docDump()
    sys.exit(0)


#########################################################
# This cmdline option overrides the setting in RC files

if neomma.MMA.options.cmdSMF is not None:
    gbl.lineno = -1
    neomma.MMA.midifuncs.setMidiFileType(["SMF=%s" % neomma.MMA.options.cmdSMF])

######################################
# Create the output filename

if not neomma.MMA.debug.noOutput:
    neomma.MMA.paths.createOutfileName(".mid")


################################################
# Read/process files....

# First the mmastart files
neomma.MMA.paths.dommaStart()

# The song file specified on the command line

if gbl.infile == 1:  # use stdin, set filename to 1
    f = 1
else:
    f = neomma.MMA.file.locFile(gbl.infile, None)

    if not f:
        gbl.lineno = -1
        error("Input file '%s' not found" % gbl.infile)

neomma.MMA.parse.parseFile(f)

# Finally, the mmaend files
neomma.MMA.paths.dommaEnd()

#################################################
# Just display the channel assignments (-c) and exit...

if neomma.MMA.debug.chshow:
    msg = ["\nFile '%s' parsed, but no MIDI file produced!" % gbl.infile]
    msg.append("\nTracks allocated:\n")
    k = list(gbl.tnames.keys())
    k.sort()
    cmax: int = max(len(a) for a in (k + gbl.deletedTracks)) + 1
    cwrap: int = 0
    for a in k:
        cwrap += cmax
        if cwrap > 60:
            cwrap = cmax
            msg.append("\n")
        msg.append(" %-*s" % (cmax, a))
    msg.append("\n")
    print(" ".join(msg))

    if gbl.deletedTracks:
        msg = ["Deleted Tracks:\n"]
        cwrap = 0
        for a in gbl.deletedTracks:
            cwrap += cmax
            if cwrap > 60:
                cwrap = cmax
                msg.append("\n")
            msg.append(
                " %-*s" % (cmax, a),
            )
        msg.append("\n")
        print(" ".join(msg))

    msg = ["Channel assignments:\n"]
    for c, n in sorted(gbl.midiAssigns.items()):
        if n:
            cwrap = 3
            msg.append(" %2s" % c)
            for nn in n:
                cwrap += cmax
                if cwrap > 63:
                    msg.append("\n    ")
                    cwrap = cmax + 3
                msg.append(" %-*s" % (cmax, nn))
            msg.append("\n")
    print(" ".join(msg))

    sys.exit(0)

neomma.MMA.writeMid.maker()

if neomma.MMA.debug.debug:
    dPrint(
        "Completed processing '%s' to '%s'." % (gbl.infile, neomma.MMA.paths.outfile)
    )
