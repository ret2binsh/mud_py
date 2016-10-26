rooms = {
    "Tavern": {
        "description": "You're in a cozy tavern warmed by an open fire.",
        "exits": { "outside": "Outside" },
    },
    "Outside": {
        "description": "You're standing outside and there is a tavern to your right and a mansion down the street. It's raining.",
        "exits": { "inside": "Tavern", "mansion": "Mansion" },
    },
    "Mansion": {
        "description": "You're on the first floor of a creepy four-story mansion.",
        "exits": {"outside": "Outside", "floor2": "Floor2"},
    },
    "Floor2": {
        "description": "You're on the second floor and filled with self doubt.",
        "exits": {"floor1": "mansion", "floor3": "Floor3"},
    },
    "Floor3": {
        "description": "You're now on floor three and have serious doubts about this place.",
        "exits": {"floor2": "Floor2", "floor4": "Floor4"},
    },
    "Floor4": {
        "description": "You're now on the top floor. A nightmarish phantom is approaching.",
        "exits": {"floor3": "Floor3", "service elevator": "Mansion"}
    }
}
