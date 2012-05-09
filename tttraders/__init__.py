# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function
__version__ = "0.0.1"


import os.path
from ttlib.paths import user_conf, user_data

from distutils.dir_util import mkpath

tttraders_parent_dir = (os.path.split(__file__))[0]
tttraders_user_conf_dir = user_conf("tttraders")
tttraders_user_data_dir = user_data("tttraders")
mkpath(tttraders_user_conf_dir)
mkpath(tttraders_user_data_dir)
def tttraders_dir(*path):
    return os.path.join(tttraders_parent_dir, *path)
def tttraders_user_conf(*local):
    return os.path.join(tttraders_user_conf_dir, *local)
def tttraders_user_data(*local):
    return os.path.join(tttraders_user_data_dir, *local)

def tttraders_kv(*path):
    Builder.load_file(tttraders_dir(*path), rulesonly=True)



import kivy


from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty

from ttlib.ttapp import TTApp

from tttraders.newgame import NewGame
from tttraders.tradersgame import TradersGame



class TTTradersApp(TTApp):
    title = "TTTraders"
    icon = os.path.join(tttraders_parent_dir, 'data/tttraders.png')
    rows = NumericProperty(0)
    cols = NumericProperty(0)
    players = NumericProperty(0)

    def data_dir(self, *args):
        return os.path.join(tttraders_parent_dir, 'data', *args)

    def __init__(self, *arg, **kwargs):
        self.app_name = 'tttraders'
        super(TTTradersApp, self).__init__(*arg, **kwargs)

    def start_game(self, config):
        self.goto_screen("game", config=config)

    def goto_screen(self, screen_name, **kwargs):
        super(TTTradersApp,self).goto_screen(screen_name, **kwargs)
        if   screen_name == "new":
            widget = NewGame( app=self )
        elif screen_name == "game":
            widget = TradersGame( app=self, **kwargs )
            widget.start_game()
        self.root.add_widget( widget )
        self.screen = screen_name

    def build_config(self, config):
        config.setdefaults('tttraders', {
            'theme': 'default'
        })

    def on_config_change(self, config, section, key, value):
        super(TTTradersApp,self).on_config_change(config, section, key, value)

    def build_settings(self, settings):
        jsondata = open(self.data_dir('settings.json')).read()
        settings.add_json_panel('TTTraders', self.config, data=jsondata)
