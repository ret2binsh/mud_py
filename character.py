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
