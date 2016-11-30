class Character(object):
    """
    Creates the generic attributes for our characters. Stores all of the
    variables such as name, current room, and authentication status. Also,
    contains all of the necessary methods that the character will need.
    """

    def __init__(self):
        # Creates generic attributes for the character

        self.name = "unknown"
        self.room = "Tavern"
        self.authenticated = False
        self.afk_status = False
        self.gold = 0
        self.level = 1
        self.exp = 0
        self.items = []

class Warrior(Character):
    """
    Creates the Warrior class which inherits all of the properties from the
    Character class.
    """

    def __init__(self):
        # Generate Warrior specific attributes
        super(Warrior,self).__init__()
        self.type = "Warrior"
        self.power = 2
        self.health = 100

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
