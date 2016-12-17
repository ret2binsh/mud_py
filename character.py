class Character(object):
    """
    Creates the generic attributes for our characters. Stores all of the
    variables such as name, current room, and authentication status. Also,
    contains all of the necessary methods that the character will need.
    """

    def __init__(self):
        # Creates generic attributes for the character

        self.name = "unknown"
        self.menu_level = 0
        self.room = "Tavern"
        self.authenticated = False
        self.muted_players = []
        self.afk_status = False
        self.gold = 0
        self.level = 1
        self.exp = 0
        self.items = []

    def __str__(self):
        # Define the default string representation of the warrior class

        return ("%s is a lvl %d %s with %d health.") % (self.name,self.level,
                                                        self.type,self.health)

    def get_items(self):
        # Iterate through the characters items and display them to the console.
        inventoryList = []    # create an empty list to hold each item
        # handles if the inventory is empty
        if not self.items:

            return "nothing but air"

        else:
            # iterates through the list which holds dictionary items
            for item in self.items:
                for key in item:
                    # append each dictionary key which is a string of the item
                    inventoryList.append(key)
            # return a string of the items list separated by a comma and a space
            return ", ".join(inventoryList)

class Warrior(Character):
    """
    Creates the Warrior class which inherits all of the properties from the
    Character class.
    """

    def __init__(self):
        # Generate Warrior specific attributes
        super(Warrior,self).__init__()
        self.type = "Warrior"
        self.power = 5
        self.health = 100
        self.defense = .9
        self.evade_chance = 20
        self.magic = 1
        self.critical = 1.2
        self.crit_chance = 10
        self.equipped_weapon = {"Fists": 10}
        self.spells = {}

class Mage(Character):
    """
    Creates the Mage class which inherits all of the properties from the
    Character class.
    """

    def __init__(self):
        #Generate Mage specific attributes
        super(Mage,self).__init__()
        self.type = "Mage"
        self.power = 1
        self.health = 90
        self.defense = .97
        self.evade_chance = 15
        self.magic = 5
        self.critical = 1.2
        self.crit_chance = 8
        self.equipped_weapon = {"Staff": 2}
        self.spells = {"Spark": 10, "Storm": 12}

class Rogue(Character):
    """
    Creates the Rogue class which inherits all of the properties from the
    Character class.
    """

    def __init__(self):
        #Generate Rogue specific attributes
        super(Rogue,self).__init__()
        self.type = "Rogue"
        self.power = 3
        self.health = 100
        self.defense = .95
        self.evade_chance = 10
        self.magic = 1
        self.critical = 1.5
        self.crit_chance = 6
        self.equipped_weapon = {"Daggers": 8}
        self.spells = {}

class Daemon(Character):
    """
    Creates the Daemon class which inherits all of the properties from the
    Character class.
    """

    def __init__(self):
        #Generate Daemon specific attributes
        super(Daemon,self).__init__()
        self.type = "Daemon"
        self.power = 6
        self.health = 80
        self.defense = .99
        self.evade_chance = 13
        self.magic = 3
        self.critical = 1.7
        self.crit_chance = 12
        self.equipped_weapon = {"Reaper": 11}
        self.spells = {"Hell Fire": 2}
