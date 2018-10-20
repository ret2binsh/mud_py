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

class Stationary_Items(object):
    """
    Creates the base class for all items that cannot be picked up. These items
    simply add to the ambience of the game world and can play a part in
    providing information about puzzles.
    """

    def __init__(self):
        # Creates generic attributes for the Stationary Items

        self.pickup_value = False

class Drink(PickUp_Items):

    def __init__(self,displayName,name,description):
    # Initiate Drink item attributes
        super(Drink,self).__init__()
        self.displayName = displayName
        self.name = name
        self.description = description
        self.consume = True
        self.equip = False
        self.healthBoost = .2

class Weapon(PickUp_Items):

    def __init__(self,displayName,name,description,power):
    # Initiate Weapon item attributes
        super(Weapon,self).__init__()
        self.displayName = displayName
        self.name = name
        self.description = description
        self.consume = False
        self.power = 10 * power
        self.equip = "weapon"
