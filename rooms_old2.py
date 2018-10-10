import time

import items

f = open('hillary.txt','r')
picture = f.read()
f.close()

rooms = {
    "Phoenix Tavern": {
        "description": "You're in a dusty tavern in Phoenix, Az. There are a few patrons but no one seems to notice you.",
        "exits": { "outside": "Downtown Phoenix", "train station": "Phoenix Train Station"},
        "items": { "beer": items.Beer(), "clock": items.Clock()} ,
    },
    "Phoenix Train Station": {
        "description": "The Phoenix train station. From here you can travel to Flagstaff, Kingman, Tucson, or Yuma.",
        "exits": {"tavern": "Phoenix Tavern"},
        "items": {"ticket booth": items.TicketBooth(), "bench": items.Bench()}
    },
    "Downtown Phoenix": {
        "description": "You're standing outside in downtown Phoenix. The sky is dusty and the sun is setting...",
        "exits": { "tavern": "Phoenix Tavern", "scottsdale": "Scottsdale", "luke afb": "Luke AFB Gate" },
        "items": {"tumbleweed": items.TumbleWeed(), "motorcycle": items.Motorcycle()}
    },
    "Luke AFB Gate": {
        "description": "You're outside the gate at Luke Air Force Base. The base appears to be overrun by ghouls.",
        "exits": { "downtown": "Downtown Phoenix"},
        "items": {"gate sign": "Welc me to Luk AFB. The premier F-16 tra ni g base!"}
    },
    "Scottsdale": {
        "description": "Welcome to Scottsdale, Arizona. This town used to be a rich suburb but has fallen into ruin since the war..",
        "exits": {"downtown": "Downtown Phoenix", "city center": "Scottsdale City Center"},
        "items": {"porsche": "This could be useful..if it wasn't broken down", "golf bag": "I may be able to use something in here..", "drug needle": "Oooh shiny."}
    },
    "Scottsdale City Center": {
        "description": "The old city center of Scottsdale. Everything looks dingy and not at all what it used to be.",
        "exits": {"fountain hills": "Fountain Hills", "mall": "Scottsdale Fashion Square Mall"},
        "items": {"light switch": "What the hell is this thing on the wall? Seems out of place.", "crooked picture": picture}
    },
    "Fountain Hills": {
        "description": "This small suburb was well known for its huge fountain at the center of the park.",
        "exits": {"scottsdale": "Scottsdale City Center", "fountain": "Fountain Area"},
        "items": {"nothing here": "nothing here"}
    },
    "Fountain Area": {
        "description": "I bet the fountain was a sight to see. Now it is just an empty basin with debris strewn about.",
        "exits": {"town": "Fountain Hills"},
        "items": {"nothing here": "nothing here"}
    },
    "Scottsdale Fashion Square Mall": {
        "description": "You're now on the top floor. A nightmarish phantom is approaching.",
        "exits": {"outside": "Scottsdale City Center", "floor2": "SFSM Floor2"},
        "items": {"sword": "Now this is what I need!!", "knife": "Uhhh not sure if this would be very useful.."}
    },
    "SFSM Floor2": {
        "description": "You're now on the top floor. A nightmarish phantom is approaching.",
        "exits": {"floor4": "Floor 4", "service elevator": "Mansion"},
        "items": {"coffee": "I need to stay awake!", "brown pants": "hmm... i might need a change of clothes if i get scared"}
    }
}
