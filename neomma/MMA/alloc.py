# alloc.py

"""
This module is an integeral part of the program
MMA - Musical Midi Accompaniment.

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

import neomma.MMA.patChord
import neomma.MMA.patWalk
import neomma.MMA.patBass
import neomma.MMA.patPlectrum
import neomma.MMA.patDrum
import neomma.MMA.patScale
import neomma.MMA.patArpeggio
import neomma.MMA.patSolo
import neomma.MMA.patAria
import neomma.MMA.grooves
import neomma.MMA.debug

from . import gbl
from neomma.MMA.common import *

trkClasses: dict[str, type] = {
    "BASS": neomma.MMA.patBass.Bass,
    "CHORD": neomma.MMA.patChord.Chord,
    "ARPEGGIO": neomma.MMA.patArpeggio.Arpeggio,
    "SCALE": neomma.MMA.patScale.Scale,
    "DRUM": neomma.MMA.patDrum.Drum,
    "WALK": neomma.MMA.patWalk.Walk,
    "MELODY": neomma.MMA.patSolo.Melody,
    "SOLO": neomma.MMA.patSolo.Solo,
    "ARIA": neomma.MMA.patAria.Aria,
    "PLECTRUM": neomma.MMA.patPlectrum.Plectrum,
}


def trackAlloc(name: str, err: bool) -> None:
    """Check existence of track and create if possible.

    If 'err' is set, the function will 'error out' if
    it's not possible to create the track. Otherwise,
    it is content to return without creation taking place.
    """

    # If the track already exists, just return

    if name in gbl.tnames:
        return

    # Get the trackname. Can be just a type, or type-name.

    if "-" in name:
        base, ext = name.split("-", 1)
    else:
        ext = None
        base = name

    """ See if there is a track class 'base'. If there is, then
        'f' points to the initialization function for the class.
        If not, we either error (err==1) or return (err==0).
    """

    try:
        f = trkClasses[base]
    except KeyError:
        if err:
            error("There is no track class '{}' for trackname '{}'".format(base, name))
        else:
            return

    # Now attempt to allocate the track

    gbl.tnames[name] = newtk = f(name)

    # Update current grooves to reflect new track.

    for slot in neomma.MMA.grooves.glist.keys():
        newtk.saveGroove(slot)

    if neomma.MMA.debug.debug:
        dPrint("Creating new track %s" % name)

    return
