# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function
from math import sqrt

from kivy.properties import ObjectProperty, NumericProperty, OptionProperty
from kivy.uix.floatlayout import FloatLayout

from ttlib.hexmap import HexMap

from tttraders import tttraders_kv
from tttraders.hex import Hex, hex_dict, random_hex

SQRT3 = sqrt(3)
SQRT3_2 = sqrt(3)/2

class Map(FloatLayout):
    hexmap_delegates = ''.split()
    hexmap = ObjectProperty(None)
    game = ObjectProperty(None)
    unit = NumericProperty(1)

    @property
    def rows(self):
        return self.hexmap.cols

    @property
    def cols(self):
        return self.hexmap.rows

    def __init__(self, **kwargs):
        super(Map, self).__init__(**kwargs)
        self.hexmap = HexMap(rows=kwargs['cols'], cols=kwargs['rows'])
        self.bind(width=self.recompute_unit, height=self.recompute_unit)
        self.bind(x=self.recompute_offsets, y=self.recompute_offsets)

    def recompute_unit(self, *args):
        # Yes, need to be reversed - hexmap orients opposite of settlers manuals
        unit = min(self.height / self.hexmap.width, self.width / self.hexmap.height)
        self.recompute_offsets()
        self.unit = unit

    def recompute_offsets(self, *args):
        self.x_off = self.x + (self.width  - self.unit * self.hexmap.height) / 2
        self.y_off = self.y + (self.height - self.unit * self.hexmap.width)  / 2

    def __getattr__(self, attrib):
        if attrib in Map.hexmap_delegates:
            return getattr(self.hexmap, attrib)


    def add_hex(self, i, j, flavor):
        hex = hex_dict[flavor](game=self.game, map=self, i=i, j=j)
        for h in self.hexmap.get(i, j, []):
            if isinstance(h,Hex):
                self.remove_widget(h)
                self.hexmap.remove_object(h)
        self.add_widget(hex)
        self.hexmap.place_object(hex, i, j, front=True)

    def add_hex_rc(self, row, col, flavor):
        self.add_hex(*self.hex_rc2ij(row, col), flavor=flavor)

    def hex_rc2ij(self, row, col):
        i = 2 * row + 1
        j = 4 * col + 2 if 0 == row % 2 else 4 * col + 4
        return (i, j)

    def address2local(self, i, j, size=(0,0)):
        """Returns local screen coordinates of addresss (i,j).
        If size is specified, coordinates will be offset by half of the size."""
        # print( str((i,j)), "at xy =", str(self.hexmap.address2xy(i, j)) )
        pos = self._unit2local( *self.hexmap.address2xy(i, j) )
        return [ pos[0] - size[0] / 2, pos[1] - size[1] / 2 ]

    def address2screen(self, i, j, size=(0,0)):
        """Returns absolute screen coordinates of addresss (i,j).
        If size is specified, coordinates will be offset by half of the size."""
        # print( str((i,j)), "at xy =", str(self.hexmap.address2xy(i, j)) )
        pos = self._unit2screen( *self.hexmap.address2xy(i, j) )
        return [ pos[0] - size[0] / 2, pos[1] - size[1] / 2 ]


    def _local2unit(self, x, y):
        """Transform a local screen coordinate (x,y) to unit coordinate (x',y')"""
        return ( self.hexmap.width - y / self.unit, x / self.unit )
    def _screen2unit(self, x, y):
        """Transform an absolute screen coordinate (x,y) to unit coordinate (x',y')"""
        return ( self.hexmap.width - (y - self.y_off) / self.unit, (x - self.x_off) / self.unit )

    def _unit2local(self, xp, yp):
        """Transform a unit coordinate (x',y') to local screen coordinate (x,y)"""
        return ( self.unit * yp, self.unit * ( self.hexmap.width  - xp ) )
    def _unit2screen(self, xp, yp):
        """Transform a unit coordinate (x',y') to absolute screen coordinate (x,y)"""
        return ( self.unit * yp + self.x_off, self.unit * ( self.hexmap.width - xp ) + self.y_off )


tttraders_kv("map.kv")
