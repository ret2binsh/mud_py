# -*- coding: utf-8 -*-

import items

# ANSI escape codes for changing the terminal colors when sending messages
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
    """ Room class object that initializes with a name, long longDescription,
    description, and a list of items that are class objects found int items.py.
    The exits attribute holds a string to send to the user for available
    neighbor rooms and is used to match against the roomExits dict.
    """

    def __init__(self):
        self.name = "Phoenix Tavern"
        self.longDescription = ("You're in a dusty tavern in Phoenix, Az. "
            "There are a few patrons but no one seems to notice you.")
        self.description = "You are in the Phoenix Tavern."
        self.items = [
            items.Drink(
                u"%sBeer%s" % (color["white"],color["reset"]),
                "Beer",
                "A delicious looking beer!"
                ),
            items.Weapon(
                u"%sDagger%s" % (color["red"],color["reset"]),
                "Dagger",
                "A rusty dagger.",
                1
                )
            ]
        self.exits = ["Phoenix Train Station"]

class PhoenixTrainStation(object):
    """ Room class object that initializes with a name, long longDescription,
    description, and a list of items that are class objects found int items.py.
    The exits attribute holds a string to send to the user for available
    neighbor rooms and is used to match against the roomExits dict.
    """

    def __init__(self):
        self.name = "Phoenix Train Station"
        self.longDescription = ("The Phoenix train station. From here you can "
            "travel to Flagstaff, Kingman, Tucson, or Yuma.")
        self.description = "This is the Phoenix Train Station."
        self.items = [
            items.Weapon(
                u"%sBuster Sword%s" % (color["red"],color["reset"]),
                "Buster Sword",
                "savage looking buster sword.",
                10
                )
            ]
        self.exits = ["Phoenix Tavern"]

# used in gamefunctions for matching the enter command parameter with an
# available room. The paramater matches the key and then the object is
# instantiated and set as the character's room attribute.
roomExits = {
    "Phoenix Tavern": PhoenixTavern(),
    "Phoenix Train Station": PhoenixTrainStation()
}
