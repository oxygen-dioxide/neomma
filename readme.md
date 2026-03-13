# Neomma

**English** | [简体中文](readme_zh.md)

Neomma is a music accompaniment generator, similar to the accompaniment function found in electronic keyboards. It can generate MIDI accompaniment tracks for soloists or singers based on user input files containing chords and MMA commands. Neomma comes with a rich collection of built-in accompaniment templates, and users can also create their own templates.
Neomma is based on [MMA—Musical MIDI Accompaniment](https://www.mellowood.ca/mma/).

## Installation

First, install [Python](https://www.python.org/), then run the following commands in the command line:

```cmd
git clone https://github.com/oxygen-dioxide/neomma
cd neomma
pip install .
```

## Usage

First, write an MMA file (a text file that declares the song's tempo, the accompaniment template to use, and the chords for each measure. For the format, see the [MMA documentation](https://www.mellowood.ca/mma/online-docs/html/tut/node3.html)).

Then run the following command in the command line:

```cmd
neomma <path-to-.mma-file>
```

The MIDI file will be output to the same directory as the MMA file.

## Development Roadmap

This repository aims to modernize MMA. Currently, Neomma differs from the original MMA in the following ways:

- Supports installation via pip
