# -*- coding: utf-8 -*-

import random

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

class Generic_Items(object):
    """
    Create the base class for all items. This will mainly handle the most
    basic functions for all items.
    """

class PickUp_Items(object):
    """
    Creates the base class for all items that can be picked up. This will
    initialize all of the generic attributes that these items will have as
    well as core functions.
    """

    def __init__(self):
        # Creates generic attributes for the PickUp Items

        self.pickup_value = True
        self.quantity = 1
        self.equip = False
        self.consume = False

class Stationary_Items(object):
    """
    Creates the base class for all items that cannot be picked up. These items
    simply add to the ambience of the game world and can play a part in
    providing information about puzzles.
    """

    def __init__(self):
        # Creates generic attributes for the Stationary Items

        self.pickup_value = False
        self.quantity = 1
        self.equip = False
        self.consume = False


class Drink(PickUp_Items):

    def __init__(self, name, description, cure_amount):
        # Initiate Drink item attributes
        super(Drink, self).__init__()
        self.name = name
        self.cure_amount = cure_amount
        self.displayName = u"%s%s%s" % (color["white"], name, color["reset"])
        self.description = description
        self.consume = True
        self.healthBoost = .2


class Weapon(PickUp_Items):

    def __init__(self, name, description, power):
        # Initiate Weapon item attributes
        super(Weapon, self).__init__()
        self.name = name
        self.displayName = u"%s%s%s" % (color["red"], name, color["reset"])
        self.description = description
        self.power = 1.2 * power
        self.equip = "weapon"


class Armor(PickUp_Items):

    def __init__(self, name, description, defense):
        # Initiate Weapon item attributes
        super(Armor, self).__init__()
        self.name = name
        self.displayName = u"%s%s%s" % (color["cyan"], name, color["reset"])
        self.description = description
        self.defense = 2 * defense
        self.equip = "armor"


class Plot_Item(Stationary_Items):

    def __init__(self, name, description, details):
        # Initiate Weapon item attributes
        super(Plot_Item, self).__init__()
        self.name = name
        self.displayName = u"%s%s%s" % (color["yellow"], name, color["reset"])
        self.description = description
        self.details = details


tier1Weapons = [
    Weapon("Dagger", "A rusty dagger.", 1),
    Weapon("Sword", "A boring sword.", 1),
    Weapon("Javelin", "A pokey weapon.", 1),
    Weapon("Pistol", "A crummy pistol.", 1)
]

tier1Armor = [
    Armor("Chain Mail", "A heavy set of chain mail.", 1),
    Armor("Leather Hide", "Crude garments made from leather.", 1),
    Armor("Black Tights",
          "\n" +
          "         ,==c==.\n" +
          "         |_/|\_|\n" +
          "         | '|` |\n" +
          "         |  |  |\n" +
          "         |  |  |\n" +
          "         |__|__|\n" +
          "\nRather tight looking pants.",
          1)
]

tier1Drinks = [
    Drink("Beer", "Warm beer\n+20HP", 20),
    Drink("Wine", "Dank wine\n+15HP", 15),
    Drink("Orange Juice", "Spoiled orange juice.\n+25HP", 25)
]

# list of tier1 items. used for random function
tier1Items = [tier1Armor, tier1Drinks, tier1Weapons]


def random_items():
    """ Function that seeds the room with a random quantity and type of
    either drink, weapon, or armor items.
    """

    itemsList = []  # list of items to be returned
    # random choice number of items. weighted towards 1 item
    for i in range(0, random.choice([1, 1, 1, 2, 3])):
        itemType = random.choice(tier1Items)
        itemsList.append(random.choice(itemType))

    return itemsList


def enemy_items():
    """
    Function that handles randomly selected the inventory
    items for an instantiated enemy.
    """

    itemType = random.choice(tier1Items)

    return random.choice(itemType)
