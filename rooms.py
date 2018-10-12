import time

import items

f = open('hillary.txt','r')
picture = f.read()
f.close()

roomExits = {
    "Phoenix Tavern": PhoenixTavern(),
    "Phoenix Train Station": PhoenixTrainStation()
}

rooms = {
    "Phoenix Tavern": {
        "description": "You're in a dusty tavern in Phoenix, Az. There are a few patrons but no one seems to notice you.",
        "exits": { "train station": "Phoenix Train Station"},
        "items": [items.Drink("Beer","A delicious looking beer!"),items.Weapon("Dagger","A rusty dagger.",1)] ,
    },
    "Phoenix Train Station": {
        "description": "The Phoenix train station. From here you can travel to Flagstaff, Kingman, Tucson, or Yuma.",
        "exits": {"tavern": "Phoenix Tavern"},
        "items": []
    }
}

class PhoenixTavern(object):
    def __init__(self):
        self.name = "Phoenix Tavern"
        self.longDescription = "You're in a dusty tavern in Phoenix, Az. There are a few patrons but no one seems to notice you."
        self.description = "You are in the Phoenix Tavern."
        self.items = [items.Drink("Beer","A delicious looking beer!"),items.Weapon("Dagger","A rusty dagger.",1)]
        self.exits = ["Phoenix Train Station"]

class PhoenixTrainStation(object):
    def __init__(self):
        self.name = "Phoenix Train Station"
        self.longDescription = "The Phoenix train station. From here you can travel to Flagstaff, Kingman, Tucson, or Yuma."
        self.description = "This is the Phoenix Train Station."
        self.items = []
        self.exits = ["Phoenix Tavern"]
