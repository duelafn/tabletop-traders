# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, absolute_import, print_function

import kivy

from kivy.factory import Factory
from kivy.properties import ObjectProperty, NumericProperty, OptionProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from ttlib.datautil import list_inserter

from tttraders import tttraders_kv
from tttraders.maploader import load_pioneers_map


class TradersGame(FloatLayout):
    Phases = ['main']
    States = set(['on_new_turn','on_step_phase'])
    ConfigTabs = []
    Config = {}

    config = ObjectProperty(None)


    @staticmethod
    def register_states(*states):
        for x in states:
            for s in ("on_enter_state_%s on_update_state_%s on_current_state_%s on_leave_state_%s" % (x,x,x,x)).split():
                TradersGame.States.update( s )

    @staticmethod
    def register_phase(phase, **where):
        if phase in TradersGame.Phases:
            raise Exception("Phase " + phase + " already exists!")
        list_inserter(TradersGame.Phases, phase, **where)

    @staticmethod
    def register_config(*settings):
        for s in settings:
            TradersGame.Config[s['tab']].append(s)
    @staticmethod
    def register_config_tab(name, **where):
        if name in TradersGame.ConfigTabs:
            raise Exception("Config tab " + name + " already exists!")
        TradersGame.Config.setdefault(name, [])
        list_inserter(TradersGame.ConfigTabs, name, **where)

    def __init__(self, **kwargs):
        super(TradersGame, self).__init__(**kwargs)
        self.states = []
        for s in TradersGame.States:
            self.register_event_type(s)

    def __getattr__(self, attrib):
        def noop(self):
            pass
        if attrib in TradersGame.States:
            return noop

    def start_game(self):
        map_str = """variant islands
title 5 - Into The Desert (V)
random-terrain
domestic-trade
check-victory-at-end-of-turn
num-players 5
sevens-rule 1
victory-points 12
num-roads 15
num-bridges 0
num-ships 15
num-settlements 5
num-cities 4
num-city-walls 3
resource-count 24
develop-road 3
develop-monopoly 3
develop-plenty 3
develop-chapel 1
develop-university 1
develop-governor 1
develop-library 1
develop-market 1
develop-soldier 19
use-pirate
chits 12,5,6,11,5,8,4,11,2,4,5,8,10,12,9,6,10,9,4,9,3,6,3,10,8,4,9,5,8,11,10,3,2
map
-,s,s,s,s,s,s,s,s,s,s
s,p0,t1,m2,h3,s,m4,h5,t6,g7+,s
-,s,s,s,d8+,d9+,d10+,d11+,d12+,s,s
s,s,s?4,so5,f13,t14,f15,t16,s?2,s,s
-,s?0,p17,h18,f19,h20,t21,m22,sl2,p23,s
s,h24,f25,m26,p27,h28,p29,s,s,s,s
-,s?0,m30,s?1,s,sb2,sw1,s,s,t31,s
s,t32,sg2,m33,f34,s,g35+,s,p36,f37,s
-,s,s,s,s,s,s,s,s,s,s
.
"""
        map = load_pioneers_map(data=map_str, parent=self)
        self.add_widget(map)

    def in_state(self,state):
        return state in self.states
    def ensure_state(self,state,*args,**kwargs):
        if state in self.states:
            print("ensure_state: Updating state", state)
            self.dispatch("on_update_state_"+state,*args,**kwargs)
        else:
            print("ensure_state: Entering state", state)
            self.push_state(state,*args,**kwargs)
    def push_state(self,state,*args,**kwargs):
        print("push_state: Entering state", state)
        self.states.append(state)
        self.dispatch("on_enter_state_"+state,*args,**kwargs)
    def remove_state(self,state,*args,**kwargs):
        if state in self.states:
            last_state = self.states[-1]
            self.states.remove(state)
            print("remove_state: Leaving state", state)
            self.dispatch("on_leave_state_"+state,*args,**kwargs)
            if self.states:
                if last_state != self.states[-1]:
                    print("remove_state: Re-entering state", self.states[-1])
                    self.dispatch("on_current_state_"+self.states[-1])
            else:
                self.step_phase()
        else:
            raise Exception("Attempt to remove non-existant state "+state)

    def step_phase(self):
        new_turn = False
        if self.phases:
            self.phase = self.phases.pop()
            print("step_phase: Entering phase", self.phase)
        else:
            self.new_turn()
        self.dispatch("on_step_phase")

    def next_turn(self):
        self.current_player_nr = (self.current_player_nr + 1) % self.nr_players
        print("next_turn:", self.current_player_nr)
        self.phases = TradersGame.Phases.reversed()
        self.phase = self.phases.pop()
        self.dispatch("on_new_turn")


import tttraders.tradersgame.base
import tttraders.tradersgame.core

Factory.register("TradersGame", TradersGame)
tttraders_kv("tradersgame.kv")
