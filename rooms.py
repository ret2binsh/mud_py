import time

from items import Beer

f = open('hillary.txt','r')
picture = f.read()
f.close()

rooms = {
    "Tavern": {
        "description": "You're in a cozy tavern warmed by an open fire.",
        "exits": { "outside": "Town", "teleporter": "Narnia"},
        "items": { "beer": str(Beer())} ,
    },
    "Narnia": {
        "description": "You find yourself in an enchanted realm, far far from everything you know",
        "exits": {"teleporter": "Tavern"},
        "items": {"broken branches": "Hmm..Evidence of a recent struggle.", "sleigh": "A means to travel quickly?"}
    },
    "Town": {
        "description": "You're standing outside and there is a tavern to your right and a mansion down the street. It's raining.",
        "exits": { "tavern": "Tavern", "mansion": "Mansion" },
        "items": {"barrel": "An old whisky barrel.", "bloody spoon": "A possible murder weapon, but who uses a spoon? Honestly?"}
    },
    "Mansion": {
        "description": "You're on the first floor of a creepy four-story mansion.",
        "exits": {"outside": "Town", "floor2": "Floor 2"},
        "items": {"candle": "This could be useful..", "chair": "A lonely chair.", "suit of armor": "Oooh shiny."}
    },
    "Floor 2": {
        "description": "You're on the second floor and filled with self doubt.",
        "exits": {"floor1": "mansion", "floor3": "Floor 3"},
        "items": {"light switch": "What the hell is this thing on the wall? Seems out of place.", "crooked picture": picture}
    },
    "Floor 3": {
        "description": "You're now on floor three and have serious doubts about this place.",
        "exits": {"floor2": "Floor 2", "floor4": "Floor 4"},
        "items": {"nothing here": "nothing here"}
    },
    "Floor 4": {
        "description": "You're now on the top floor. A nightmarish phantom is approaching.",
        "exits": {"floor3": "Floor 3", "floor5": "Floor 5"},
        "items": {"sword": "Now this is what I need!!", "knife": "Uhhh not sure if this would be very useful.."}
    },
    "Floor 5": {
        "description": "You're now on the top floor. A nightmarish phantom is approaching.",
        "exits": {"floor4": "Floor 4", "service elevator": "Mansion"},
        "items": {"coffee": "I need to stay awake!", "brown pants": "hmm... i might need a change of clothes if i get scared"}
    }
}
