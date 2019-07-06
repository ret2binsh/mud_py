import rooms
import copy

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

class Fists(object):
    """
    Simple class to use for when the character does not have a weapon equipped.
    This will be added to the character.equpped_weapon attribute when using
    the unequip command.
    """

    def __init__(self):

        self.name = "Fists"
        self.description = "wimpy looking fists"
        self.power = 1

class Naked(object):
    """
    Class for keeping track of when the user does not have armor equipped.
    """

    def __init__(self):

        self.name = "Bday Suit"
        self.description = "absolutely nothing"
        self.defense = 0

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
        self.room = rooms.OasisLobby()
        self.authenticated = False
        self.muted_players = []
        self.afk_status = False
        self.credits = 0
        self.level = 1
        self.exp = 0
        self.inventory = []
        self.equipped_weapon = Fists()
        self.equipped_armor = Naked()

    def __str__(self):
        # Define the default string representation of the warrior class

        return ("%s is a lvl %d %s with %d health.") % (self.name,self.level,
                                                        self.type,self.health)

    def equip(self,choice):
        # equips either a weapon or armor and updates the power/def
        # also removes the item from inventory and return a boolean to
        # determine which message to send

        for item in self.inventory:

            if item.name == choice and item.equip == "armor":

                # if already equipped send the default message that the item
                # has been equipped but don't do anything. change this in the
                # future to say a different message.
                if self.equipped_armor.name == choice:
                    return True

                # swaps item back into inventory if it isn't the default armor
                # if equipped item exists in inventory then +1 the quantity
                if self.equipped_armor.name != "Bday Suit":
                    for old in self.inventory:
                        if old.name == self.equipped_armor.name:
                            old.quantity = old.quantity + 1
                            break

                    else:
                        self.inventory.append(self.equipped_armor)

                # if the item to be equipped has a quantity greater than 1
                # then copy the object into the equipped slot, set it's
                # quantity to 1 and decrement the inventory by 1
                if item.quantity > 1:
                    self.equipped_armor = copy.deepcopy(item)
                    self.equipped_armor.quantity = 1
                    item.quantity = item.quantity - 1
                    self.defense = self.base_defense * self.equipped_armor.defense
                    return True

                # if the item isn't currently equipped and it's quantity is 1
                # then set the equipped slot to the item and remove it from the
                # inventory
                self.equipped_armor = item
                self.defense = self.base_defense * self.equipped_armor.defense
                self.inventory.remove(item)
                return True

            elif item.name == choice and item.equip == "weapon":
                # if already equipped send the default message that the item
                # has been equipped but don't do anything. change this in the
                # future to say a different message.
                if self.equipped_weapon.name == choice:
                    return True

                # swaps item back into inventory if it isn't the default weapon
                # if equipped item exists in inventory then +1 the quantity
                if self.equipped_weapon.name != "Fists":
                    for old in self.inventory:
                        if old.name == self.equipped_weapon.name:
                            old.quantity = old.quantity + 1
                            break

                    else:
                        self.inventory.append(self.equipped_weapon)

                # if the item to be equipped has a quantity greater than 1
                # then copy the object into the equipped slot, set it's
                # quantity to 1 and decrement the inventory by 1
                if item.quantity > 1:
                    self.equipped_weapon = copy.deepcopy(item)
                    self.equipped_weapon.quantity = 1
                    item.quantity = item.quantity - 1
                    self.power = self.base_power * self.equipped_weapon.power
                    return True

                # if the item isn't currently equipped and it's quantity is 1
                # then set the equipped slot to the item and remove it from the
                # inventory
                self.equipped_weapon = item
                self.power = self.base_power * self.equipped_weapon.power
                self.inventory.remove(item)
                return True

        return False

    def  unequip(self,choice):
        # unequips item, equips default gear, resets defense/power, places item
        # back in inventory and returns boolean to decide which message to send
        # the user

        # used to shorten the variables
        armorName = self.equipped_armor.name
        weaponName = self.equipped_weapon.name

        # determine the armor is equipped and not the default 'armor'
        if choice == armorName and armorName != "Bday Suit":
            # increment item in inventory if multiples exist
            for item in self.inventory:
                if item.name == choice:
                    item.quantity = item.quantity + 1
                    break   # break for loop so item isn't appended
            else:
                self.inventory.append(self.equipped_armor)

            # equip default 'armor' and recalculate defense
            self.equipped_armor = Naked()
            self.defense = self.base_defense * self.equipped_armor.defense
            return True

        # determine the weapon is equipped and not the default weapon
        elif choice == weaponName and weaponName != "Fists":
            # increment item in inventory if multiples exist
            for item in self.inventory:
                if item.name == choice:
                    item.quantity = item.quantity + 1
                    break   # break for loop so item isn't appended
            else:
                self.inventory.append(self.equipped_weapon)

            # equip default weapon and recalculate power
            self.equipped_weapon = Fists()
            self.power = self.base_power * self.equipped_weapon.power
            return True

        else:
            # if not a valid option or default equip: return False
            # to send the failed to unequip message
            return False


    def get_items(self):
        # Iterate through the characters items and display them to the console.
        inventoryList = []    # create an empty list to hold each item
        # handles if the inventory is empty
        if not self.inventory:

            return ["nothing but air"]

        else:
            # iterates through the list which holds dictionary items
            for item in self.inventory:
                # append each dictionary key which is a string of the item
                inventoryList.append(("%s[%d]") % (item.displayName,item.quantity))
            inventoryList.sort() # sort the inventory alphabetically
            return inventoryList

    def get_status(self):

        # determine the offset lengths for all left-side dynamic numbers
        a = len(str(self.health)) + len(str(self.max_health))
        b = len(str(self.exp))
        c = len(str(self.base_power)) + len(str(self.equipped_weapon.power)) + len(str(self.power))
        d = len(str(self.base_defense)) + len(str(self.equipped_armor.defense)) + len(str(self.defense))

        # multipled spaces and subtracted them by the dynamic length of the left-side Variables
        # this ensures everything stays nicely formatted. Returns a list of strings
        status_screen = ["********************************************************************************",
                         " Name    :  {0}{1}{2}".format(color["yellow"],self.name,color["reset"]),
                         " Credits :  {0}{1}{2}".format(color["yellow"],self.credits,color["reset"]),
                         " Level   :  {0}{1}{2}    Class :  {3}{4}{5}     Current Room :  {6}{7}{8}".format(color["yellow"],
                            self.level,color["reset"],color["yellow"],self.type,color["reset"],color["yellow"],self.room.name,color["reset"]),
                         "********************************************************************************",
                         (" Health     :  {0}{1}{2}/{3}{4}{5}" + " "*(37-a) + "Weapon:  {6}{7}{8}").format(color["red"],
                         self.health,color["reset"],color["yellow"],self.max_health,color["reset"],color["red"],self.equipped_weapon.name,color["reset"]),
                         (" Experience :  {0}{1}{2}" + " "*(38-b) + "Armor :  {3}{4}{5}").format(color["yellow"],
                         self.exp,color["reset"],color["red"],self.equipped_armor.name,color["reset"]),
                         "********************************************************************************",
                         (" Attack Power :  {0}({1}{2}{3})/{4}" + " "*(33-c) + "Critical :  {5}{6}{7}").format(self.base_power,
                         color["blue"],self.equipped_weapon.power,color["reset"],self.power,color["blue"],self.critical,color["reset"]),
                         (" Defense      :  {0}({1}{2}{3})/{4}" + " "*(33-d) + "Crit %   :  {5}{6}{7}").format(self.base_defense,
                         color["blue"],self.equipped_armor.defense,color["reset"],self.defense,color["blue"],self.crit_chance,color["reset"]),
                         "********************************************************************************"]

        return status_screen

class Warrior(Character):
    """
    Creates the Warrior class which inherits all of the properties from the
    Character class.
    """

    def __init__(self):
        # Generate Warrior specific attributes
        super(Warrior,self).__init__()
        self.type = "Warrior"
        self.base_power = 1
        self.power = self.base_power * self.equipped_weapon.power
        self.health = 100
        self.max_health = 100
        self.base_defense = .9
        self.defense = self.base_defense * self.equipped_armor.defense
        self.evade_chance = 20
        self.magic = 1
        self.critical = 1.2
        self.crit_chance = 10
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
        self.max_health = 90
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
        self.max_health = 100
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
        self.max_health = 80
        self.defense = .99
        self.evade_chance = 13
        self.magic = 3
        self.critical = 1.7
        self.crit_chance = 12
        self.equipped_weapon = {"Reaper": 11}
        self.spells = {"Hell Fire": 2}
