# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function
from random import choice
from math import sqrt

import kivy
import numpy

from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, ReferenceListProperty, NumericProperty
from kivy.uix.image import Image

from tttraders import tttraders_kv


hex_dict = {}
def register_hex(name, cls):
    hex_dict[name] = cls

def random_hex(**kwargs):
    choice(hex_dict.values())

SQRT3 = sqrt(3)

class Hex(Image):
    game = ObjectProperty(None)
    map  = ObjectProperty(None)
    hex_name = StringProperty(None)
    i = NumericProperty(0)
    j = NumericProperty(0)
    address = ReferenceListProperty(i, j)

    def __init__(self, **kwargs):
        kwargs.setdefault('hex_name', self.__class__.__name__.replace('Hex',''))
        kwargs.setdefault('source', 'Hex' + kwargs['hex_name'] + '.png')
        super(Hex,self).__init__(**kwargs)
        self.map.bind(unit=self.on_change_unit)
        self.map.bind(x=self.on_change_pos,y=self.on_change_pos)

    def on_change_unit(self, obj, unit):
        self.width  = SQRT3 * unit
        self.height = 2 * unit
        self.rel_pos = self.map.address2local(self.i, self.j, size=self.size)
        self.on_change_pos(self,1)

    def on_change_pos(self, obj, unit):
        self.x = self.map.x_off + self.rel_pos[0]
        self.y = self.map.y_off + self.rel_pos[1]


tttraders_kv("hex.kv")


# Gold, Wood, Wheat, Sheep, Stone, Brick
# Paper, Cloth, Coin
class DesertHex(Hex):
    pass
register_hex("Desert", DesertHex)

class FarmlandHex(Hex):
    pass
register_hex("Farmland", FarmlandHex)

class ForestHex(Hex):
    pass
register_hex("Forest", ForestHex)

class GoldHex(Hex):
    pass
register_hex("Gold", GoldHex)

class HillHex(Hex):
    pass
register_hex("Hill", HillHex)

class MountainHex(Hex):
    pass
register_hex("Mountain", MountainHex)

class PastureHex(Hex):
    pass
register_hex("Pasture", PastureHex)

class WaterHex(Hex):
    pass
register_hex("Water", WaterHex)
