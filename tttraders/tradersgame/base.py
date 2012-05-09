# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

from tttraders.tradersgame import TradersGame


TradersGame.register_config_tab('Main')
TradersGame.register_config(
    {
        "type": "int",
        "title": "Rows",
        "desc": "Number of hex rows",
        "section": "main",
        "key": "rows",
        "default": '5',
        "tab": "Main",
        },
    {
        "type": "int",
        "title": "Columns",
        "desc": "Number of hex columns",
        "section": "main",
        "key": "columns",
        "default": '10',
        "tab": "Main",
        },
    {
        "type": "int",
        "title": "Players",
        "desc": "Number of players",
        "section": "main",
        "key": "nr_players",
        "default": '4',
        "tab": "Main",
        },
    )
