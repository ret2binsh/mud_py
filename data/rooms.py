import items

class Rooms(object):
    """ Parent class that holds all of the methods that each child room
    class will inherit.
    """

    def enter_room(self,choice):
        # returns a room object using the roomExits dictionary

        return roomExits[choice]

class PhoenixTavern(object):
    """ Room class object that initializes with a name, long longDescription,
    description, and a list of items that are class objects found int items.py.
    The exits attribute holds a string to send to the user for available
    neighbor rooms and is used to match against the roomExits dict.
    """

    def __init__(self):
        super(PhoenixTavern,self).__init__()
        self.name = "Phoenix Tavern"
        self.longDescription = ("You're in a dusty tavern in Phoenix, Az. "
            "There are a few patrons but no one seems to notice you.")
        self.description = "You are in the Phoenix Tavern."
        self.items = items.random_items()
        self.exits = ["Phoenix Train Station"]

class PhoenixTrainStation(object):
    """ Room class object that initializes with a name, long longDescription,
    description, and a list of items that are class objects found int items.py.
    The exits attribute holds a string to send to the user for available
    neighbor rooms and is used to match against the roomExits dict.
    """

    def __init__(self):
        super(PhoenixTrainStation,self).__init__()
        self.name = "Phoenix Train Station"
        self.longDescription = ("The Phoenix train station. From here you can "
            "travel to Flagstaff, Kingman, Tucson, or Yuma.")
        self.description = "This is the Phoenix Train Station."
        self.items = items.random_items()
        self.exits = ["Phoenix Tavern"]

# used in gamefunctions for matching the enter command parameter with an
# available room. The paramater matches the key and then the object is
# instantiated and set as the character's room attribute.
roomExits = {
    "Phoenix Tavern": PhoenixTavern(),
    "Phoenix Train Station": PhoenixTrainStation()
}
