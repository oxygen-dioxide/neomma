# tweaks.py

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

This module has support for some simple default tweaks.

"""

from neomma.MMA.common import *
import neomma.MMA.midiC

import copy

def setTweak(ln:list[str]) -> None:
    """ Option tweaks. """

    import neomma.MMA.pat   # here to avoid a circular dep problem
    from neomma.MMA.miditables import drumKits
   

    notopt, opts = opt2pair(ln)

    if notopt:
        error("Tweaks: expecting cmd=opt pairs, not '%s'." % ' '.join(notopt))

    for cmd, opt_str in opts:
        cmd = cmd.upper()

        if cmd in ('DEFAULTDRUM', 'DEFAULTTONE'):
            neomma.MMA.pat.defaultDrum = neomma.MMA.midiC.decodeVoice(opt_str)

        elif cmd == 'DEFAULTVOICE':
            neomma.MMA.pat.defaultVoice = neomma.MMA.midiC.decodeVoice(opt_str)

        elif cmd == 'DRUMKIT':
            opt_str = opt_str.upper()
            if opt_str.endswith('KIT'):  # optional, end kit name with 'KIT'
                opt_str = opt_str[:-3]
            if opt_str in drumKits:
                opt = drumKits[opt_str]
            else:
                opt = stoi(opt_str)
                if opt < 0 or opt > 127:
                    error("Tweaks DrumKit: value must be 0..127 not '%s'." % opt)
                    
            neomma.MMA.pat.defaultDrum = opt
            
        elif cmd == 'DIM':
            from neomma.MMA.chordtable import chordlist, Chord

            if opt_str == '3':
                # this is so we can change the desc. (no non-standard)
                chordlist['dim'] = Chord(chordlist['dim3'].chord, chordlist['dim3'].scale, "Diminished triad")
            elif opt_str == '7':
                chordlist['dim'] = copy.deepcopy(chordlist['dim7'])
            else:
                error("Tweaks: DIM requires '3' or '7' arg, not '%s'." % opt_str)

        elif cmd == 'PLECTRUMRESET':
            import neomma.MMA.patPlectrum
            neomma.MMA.patPlectrum.plectrumReset = getTF(opt_str, "Tweaks PlectrumReset")
            
        else:
            error("Tweaks: '%s' unknown command." % cmd)
