# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import kivy
import json

from kivy.config import ConfigParser
from kivy.factory import Factory
from kivy.properties import ObjectProperty, NumericProperty, OptionProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.settings import Settings

from ttlib.ttsettingint import TTSettingInt

from tttraders import tttraders_kv, tttraders_user_conf
from tttraders.tradersgame import TradersGame


class NewGame(AnchorLayout):
    app = ObjectProperty(None)
    config = ObjectProperty(None)
    settings = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(NewGame, self).__init__(**kwargs)
        self.config = ConfigParser()
        self.config.read(tttraders_user_conf('tttraders.ini'))

        self.settings.register_type("int", TTSettingInt)

        for tab in TradersGame.ConfigTabs:
            lst  = TradersGame.Config[tab]
            for c in lst:
                if c.get("key", None):
                    self.config.adddefaultsection(c['section'])
                    self.config.setdefault(c['section'], c['key'], c.get("default", None))
            self.settings.add_json_panel(tab, self.config, data=json.dumps(lst))


Factory.register("NewGame", NewGame)
tttraders_kv("newgame.kv")
