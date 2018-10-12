# -*- coding: utf-8 -*-

import time
import items
"""
f = open('hillary.txt','r')
picture = f.read()
f.close()
"""

color = {
    "black": u"\u001b[30;1m",
    "red": u"\u001b[31;1m",
    "green": u"\u001b[32;1m",
    "yellow": u"\u001b[33;1m",
    "blue": u"\u001b[34;1m",
    "magenta": u"\u001b[35;1m",
    "cyan": u"\u001b[36;1m",
    "white": u"\u001b[37;1m",
    "reset": u"\u001b[0m"

}

class PhoenixTavern(object):
    def __init__(self):
        self.name = "Phoenix Tavern"
        self.longDescription = "You're in a dusty tavern in Phoenix, Az. There are a few patrons but no one seems to notice you."
        self.description = "You are in the Phoenix Tavern."
        self.items = [items.Drink(u"%sBeer%s" % (color["white"],color["reset"]),"A delicious looking beer!"),items.Weapon(u"%sDagger%s" % (color["green"],color["reset"]),"A rusty dagger.",1)]
        self.exits = ["Phoenix Train Station"]

class PhoenixTrainStation(object):
    def __init__(self):
        self.name = "Phoenix Train Station"
        self.longDescription = "The Phoenix train station. From here you can travel to Flagstaff, Kingman, Tucson, or Yuma."
        self.description = "This is the Phoenix Train Station."
        self.items = []
        self.exits = ["Phoenix Tavern"]


roomExits = {
    "Phoenix Tavern": PhoenixTavern(),
    "Phoenix Train Station": PhoenixTrainStation()
}
