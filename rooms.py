rooms = {
    "Tavern": {
        "description": "You're in a cozy tavern warmed by an open fire.",
        "exits": { "outside": "Town", "teleporter", "Narnia"},
        "items": {"beer": "beer", "barstool": "barstool","clock": "clock"} ,
    },
    "Narnia": {
        "description": "You find yourself in an enchanted realm, far far from everything you know",
        "exits": {"teleporter": "Tavern"},
        "items": {"broken branches": "broken branches", "sleigh": "sleigh"}
    }
    "Town": {
        "description": "You're standing outside and there is a tavern to your right and a mansion down the street. It's raining.",
        "exits": { "tavern": "Tavern", "mansion": "Mansion" },
        "items": {"barrel": "barrel", "bloody spoon": "bloody spoon"}
    },
    "Mansion": {
        "description": "You're on the first floor of a creepy four-story mansion.",
        "exits": {"outside": "Town", "floor2": "Floor2"},
        "items": {"candle": "candle", "chair": "chair", "suit of armor": "suit of armor"}
    },
    "Floor2": {
        "description": "You're on the second floor and filled with self doubt.",
        "exits": {"floor1": "mansion", "floor3": "Floor3"},
        "items": {"light switch": "light switch", "crooked picture": "crooked picture"}
    },
    "Floor3": {
        "description": "You're now on floor three and have serious doubts about this place.",
        "exits": {"floor2": "Floor2", "floor4": "Floor4"},
        "items": {"nothing here": "nothing here"}
    },
    "Floor4": {
        "description": "You're now on the top floor. A nightmarish phantom is approaching.",
        "exits": {"floor3": "Floor3", "service elevator": "Mansion"}
        "items": {"sword": "sword", "knife": "knife"}
    }
}
