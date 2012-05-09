# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import re

from tttraders.hex import hex_dict, random_hex
from tttraders.map import Map

symbol = {
    'g': 'Gold',
    's': 'Water',
    'd': 'Desert',
    'p': 'Pasture',
    'm': 'Mountain',
    'f': 'Farmland',
    'h': 'Hill',
    't': 'Forest',
    '-': None,
    }

pat = {
    "ignore": re.compile(r'^\s*(?:#|$|nosetup )'),
    "key-value": re.compile(r'^(\S+)\s+(.+)'),
    "bool-opt": re.compile(r'^(\S+)$'),
    "begin-map": re.compile(r'^map$'),
    "end-map": re.compile(r'^\.$'),
    }

def load_pioneers_map(**kwargs):
    if kwargs.get('data',None):
        data = kwargs['data'].split("\n")
    elif kwargs.get('file',None):
        data = open(kwargs['file']).read().split("\n")

    # Parse the map file
    in_map = False
    rows = 0
    cols = 0
    tiles = []
    for l in data:
        if in_map:
            if pat['end-map'].match(l):
                in_map = False
            else:
                row = l.split(',')
                rows += 1
                cols = max(cols, len(row))
                tiles.append(row)

        elif pat['ignore'].match(l):
            pass
        elif pat['key-value'].match(l):
            pass
        elif pat['begin-map'].match(l):
            in_map = True
        elif pat['bool-opt'].match(l):
            pass
        else:
            raise Exception("Can not parse map file line: " + l)

    # Build map object
    map = Map(rows=rows, cols=cols, **kwargs)

    for r in xrange(rows):
        for c in xrange(cols):
            if symbol[tiles[r][c][0]]:
                map.add_hex_rc(r, c, symbol[tiles[r][c][0]])

    return map
