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

class Stationary_Items(object):
    """
    Creates the base class for all items that cannot be picked up. These items
    simply add to the ambience of the game world and can play a part in
    providing information about puzzles.
    """

    def __init__(self):
        # Creates generic attributes for the Stationary Items

        self.pickup_value = False

class Beer(Stationary_Items):

    def __init__(self):
    # Initiate Beer item attributes
        super(Beer,self).__init__()
        self.name = "Beer"
        self.description = "A delicious looking wheat beer."

    def __str__(self):
        # Define what the default string repesentation for the Beer Items
        return ("%s: %s") % (self.name,self.description)

class Clock(Stationary_Items):

    def __init__(self):
    # Initiate Beer item attributes
        super(Clock,self).__init__()
        self.name = "Clock"
        self.description = "The clock is stuck at 13:37."

    def __str__(self):
        # Define what the default string repesentation for the Beer Items
        return ("%s: %s") % (self.name,self.description)

class TicketBooth(Stationary_Items):

    def __init__(self):
    # Initiate Beer item attributes
        super(TicketBooth,self).__init__()
        self.name = "Ticket Booth"
        self.description = "Purchase your tickets here!"

    def __str__(self):
        # Define what the default string repesentation for the Beer Items
        return ("%s: %s") % (self.name,self.description)

class Bench(Stationary_Items):

    def __init__(self):
    # Initiate Beer item attributes
        super(Bench,self).__init__()
        self.name = "Bench"
        self.description = "There is a rugged bum sleeping here."

    def __str__(self):
        # Define what the default string repesentation for the Beer Items
        return ("%s: %s") % (self.name,self.description)

class TumbleWeed(Stationary_Items):

    def __init__(self):
    # Initiate Beer item attributes
        super(TumbleWeed,self).__init__()
        self.name = "TumbleWeed"
        self.description = "There's a weapon in here!"

    def __str__(self):
        # Define what the default string repesentation for the Beer Items
        return ("%s: %s") % (self.name,self.description)

class Motorcycle(Stationary_Items):

    def __init__(self):
    # Initiate Beer item attributes
        super(Motorcycle,self).__init__()
        self.name = "Motorcycle"
        self.description = "Old and broken down. Nothing to see here."

    def __str__(self):
        # Define what the default string repesentation for the Beer Items
        return ("%s: %s") % (self.name,self.description)
