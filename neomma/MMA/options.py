# options.py

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

import sys

from . import gbl
from neomma.MMA.common import *
from neomma.MMA.macro import macros
cmdSMF = None


def setBarRange(v):
    """ Set a range of bars to compile. This is the -B/b option."""
    
    if gbl.barRange:
        error("Only one -b or -B permitted.")

    for ll in v.split(','):

        l = ll.split("-")

        if len(l) == 2:
            s, e = l
            try:
                s = int(s)
                e = int(e)
            except:
                error("-B/b ranges must be integers, not '%s'." % l)

            for a in range(s, e + 1):
                gbl.barRange.append(str(a))

        elif len(l) == 1:
            try:
                s = int(l[0])
            except:
                error("-B/b range must be an integer, not '%s'." % l[0])
            gbl.barRange.append(str(s))

        else:
            error("-B/b option expecting N1-N2,N3... not '%s'." % v)


def handle_doc_option(doc_type):
    """Handle --doc option for documentation extraction."""
    import neomma.MMA.alloc
    import neomma.MMA.parse

    if doc_type == "keywords":
        print(
            "Base track names: %s \n"
            % " ".join([a for a in sorted(neomma.MMA.alloc.trkClasses)])
        )
        print(
            "Commands: %s BEGIN END DEFAULT\n"
            % " ".join([a for a in sorted(neomma.MMA.parse.simpleFuncs)])
        )
        print(
            "TrackCommands: %s \n"
            % " ".join([a for a in sorted(neomma.MMA.parse.trackFuncs)])
        )
        print("Not complete ... subcommands, comments, chords...")
        sys.exit(0)
    elif doc_type == "latex":
        gbl.createDocs = 1
    elif doc_type == "html":
        gbl.createDocs = 2
    elif doc_type == "sequence":
        gbl.createDocs = 3
    elif doc_type == "json":
        gbl.createDocs = 5
    elif doc_type == "grooves":
        gbl.createDocs = 99
    else:
        error("Invalid doc type '%s' for --doc option." % doc_type)


def handle_xoption(xopt, args):
    """Handle extended options (formerly -x)."""
    import neomma.MMA.xtra

    neomma.MMA.xtra.xoption(xopt, args)


import click


@click.command()
@click.option(
    "-b", "--bar-range", help="Limit compilation to bar range (comment numbers)"
)
@click.option(
    "-B", "--bar-range-abs", help="Limit compilation to bar range (absolute numbers)"
)
@click.option(
    "-c", "--show-channels", is_flag=True, help="Display default Channel assignments"
)
@click.option("-d", "--debug", is_flag=True, help="Enable debugging messages")
@click.option(
    "-D", "--doc",
    type=click.Choice(["keywords", "latex", "html", "json", "sequence", "grooves"]),
    help="Extract documentation: keywords, latex, html, json, sequence, grooves",
)
@click.option("-e", "--show-expanded", is_flag=True, help="Show parsed/Expanded lines")
@click.option("-f", "--output", type=click.Path(), help="Set output filename")
@click.option(
    "-g", "--groove-db", is_flag=True, help="Update Groove dependency database"
)
@click.option(
    "-G", "--create-groove-db", is_flag=True, help="Create Groove dependency database"
)
@click.option(
    "-i", "--init", type=click.Path(exists=True), help="Specify init (mmarc) file"
)
@click.option(
    "-L", "--show-bar-order", is_flag=True, help="Show order of bars processed"
)
@click.option(
    "-m", "--max-bars", type=int, help="Set maximum number of bars (default: 500)"
)
@click.option("-M", "--smf", type=click.Choice(["0", "1"]), help="Set SMF to 0 or 1")
@click.option("-n", "--no-output", is_flag=True, help="No generation of midi output")
@click.option(
    "-p", "--show-patterns", is_flag=True, help="Display Patterns as they are defined"
)
@click.option("-P", "--play", is_flag=True, help="Play song with player (dont save)")
@click.option("-r", "--show-progress", is_flag=True, help="Display running progress")
@click.option(
    "-s", "--show-sequence", is_flag=True, help="Display Sequence info during run"
)
@click.option(
    "-S", "--set-macro", multiple=True, help="Set macro 'var' to 'data'"
)
@click.option(
    "-T", "--tracks", help="Limit generation to specified tracks (comma-separated)"
)
@click.option("-w", "--no-warnings", is_flag=True, help="Disable Warning messages")
@click.option("--tsplit", is_flag=True, help="Create midi for each track")
@click.option("--csplit", is_flag=True, help="Create MIDI for each channel")
@click.option("--nocredit", is_flag=True, help="Disable MMA credits in Midi Meta track")
@click.option(
    "--syncstart", is_flag=True, help="Create sync at start of all channel tracks"
)
@click.option(
    "--syncend", is_flag=True, help="Create sync at end of all channel tracks"
)
@click.option("-v", "--version", is_flag=True, help="Display version number")
@click.argument("infile", required=False)
def cli(
    bar_range:str,
    bar_range_abs:str,
    output:str,
    init:str,
    no_output:bool,
    play:bool,
    show_channels:bool,
    debug:bool,
    show_expanded:bool,
    show_patterns:bool,
    show_progress:bool,
    show_sequence:bool,
    show_bar_order:bool,
    no_warnings:bool,
    smf:str,
    tracks:str,
    groove_db:bool,
    create_groove_db:bool,
    doc:str,
    tsplit:bool,
    csplit:bool,
    nocredit:bool,
    syncstart:bool,
    syncend:bool,
    version:bool,
    infile:str,
    set_macro:list[str],
):
    """MMA - Musical Midi Accompaniment.

    Generate MIDI accompaniment from simple chord and groove definitions.
    """
    if version:
        print("%s" % gbl.version)
        sys.exit(0)

    if bar_range:
        setBarRange(bar_range)

    if bar_range_abs:
        setBarRange(bar_range_abs)
        gbl.barRange.append("ABS")

    if output:
        gbl.outfile = output

    if init:
        neomma.MMA.paths.setRC(init)

    if no_output:
        import neomma.MMA.debug

        neomma.MMA.debug.cmdLineDebug("n")

    if play:
        gbl.playFile = 1

    if show_channels:
        import neomma.MMA.debug

        neomma.MMA.debug.cmdLineDebug("c")

    if debug:
        import neomma.MMA.debug

        neomma.MMA.debug.cmdLineDebug("d")

    if show_expanded:
        import neomma.MMA.debug

        neomma.MMA.debug.cmdLineDebug("e")

    if show_patterns:
        import neomma.MMA.debug

        neomma.MMA.debug.cmdLineDebug("p")

    if show_progress:
        import neomma.MMA.debug

        neomma.MMA.debug.cmdLineDebug("r")

    if show_sequence:
        import neomma.MMA.debug

        neomma.MMA.debug.cmdLineDebug("s")
    
    for opt in set_macro:
        macros.setvar(opt.split("=", 1))

    if show_bar_order:
        gbl.printProcessed = True

    if no_warnings:
        import neomma.MMA.debug

        neomma.MMA.debug.cmdLineDebug("w")

    global cmdSMF
    if smf:
        if smf in ["0", "1"]:
            cmdSMF = smf
        else:
            error("Only a '0' or '1' is permitted for the --smf option")

    if tracks:
        gbl.muteTracks = tracks.upper().split(",")

    if groove_db:
        gbl.makeGrvDefs = 1

    if create_groove_db:
        gbl.makeGrvDefs = 2

    if doc:
        handle_doc_option(doc)

    if tsplit:
        handle_xoption("TSplit", [])

    if csplit:
        handle_xoption("CSplit", [])

    if nocredit:
        handle_xoption("NOCREDIT", [])

    if syncstart:
        import neomma.MMA.sync

        neomma.MMA.sync.synchronize(["START"])

    if syncend:
        import neomma.MMA.sync

        neomma.MMA.sync.synchronize(["END"])

    if infile and infile != "-":
        gbl.infile = infile
    elif infile == "-":
        gbl.infile = 1

    if gbl.infile == 1 and not gbl.outfile:
        import neomma.MMA.debug

        if not neomma.MMA.debug.noOutput:
            error("Input from STDIN specified. Use --output to set an output filename.")
