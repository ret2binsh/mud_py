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
