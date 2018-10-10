import time

import items

f = open('hillary.txt','r')
picture = f.read()
f.close()

rooms = {
    "Phoenix Tavern": {
        "description": "You're in a dusty tavern in Phoenix, Az. There are a few patrons but no one seems to notice you.",
        "exits": { "outside": "Downtown Phoenix", "train station": "Phoenix Train Station"},
        "items": [items.Drink("Beer","A delicious looking beer!")] ,
    },
    "Phoenix Train Station": {
        "description": "The Phoenix train station. From here you can travel to Flagstaff, Kingman, Tucson, or Yuma.",
        "exits": {"tavern": "Phoenix Tavern"},
        "items": []
    }
}
