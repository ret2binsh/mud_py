import hashlib

from character import Warrior
from banner import bannerText

# empty list for tracking all players
players = {}

# ansi escape color codes
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

def login_check(mud,user,command):
    """
    Reads the server password hash file and compares the user provided
    password against it. The user's authentication status will be set to True
    once the correct password is entered.
    """

    # Get server hash from pass file.
    file_conn = open('data/pass', 'r')
    serverSecret = file_conn.readline()
    file_conn.close()

    # Compare user provide password against the stored hash
    hashResult = hashlib.sha224(command).hexdigest()
    if hashResult != serverSecret:
        mud.send_message(user, "Sorry, you provided an incorrect password.")
    else:
        players[user].authenticated = mud.authentication_status(user,True)
        mud.send_message(user, "Welcome!")
        mud.send_message(user, "What is your name?")

def new_players_check(mud):
    """
    Checks to see if there are new players that have joined the server.
    Displays a banner and adds the user to the list of players.
    """

    # go through any newly connected players
    for user in mud.get_new_players():

        # add the new player to the dictionary using the Character class.
        # all default attributes are loaded and stored within the Character
        # object that can be accessed using the id key.
        players[user] = Warrior()

        # send the new player the game banner
        for line in bannerText:

            mud.send_message(user, line)

        # send the new player a prompt for the server password
        mud.send_message(user,"%sPlease enter the login password:%s" % (color["red"],color["reset"]))

def disconnected_players_check(mud):
    """
    Checks for disconnected players. If there are any then they are removed
    from the players dictionary.
    """

    # go through any recently disconnected players
    for user in mud.get_disconnected_players():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if user not in players: continue

        # go through all the players in the game
        for pid,pl in players.items():
            # send each player a message to tell them about the diconnected player
            mud.send_message(pid,"%s quit the game" % players[user].name)

        # remove the player's entry in the player dictionary
        del(players[user])

def process_commands(mud):
    """
    The main game function that handles all received commands. This will be
    processed in a tiered approach to determine which state the player is in:
    either normal, store, battle, etc.
    """

    # Contstant Variables used to track the mode that the user is currently
    # operating.
    _LOGIN_MODE = 0
    _CHARACTER_SELECT_MODE = 1
    _EXPLORATION_MODE = 2
    _BATTLE_MODE = 3
    _STORE_MODE = 4
    _INN_MODE = 5

    # go through any new commands sent from players
    for user,command,params in mud.get_commands():

        # arguments list used for the command list
        args = [mud,user,command,params]

        # List of commands when in normal mode
        command_list = {
            "enter": enter_command,
            "e": enter_command,
            "equip": equip_command,
            "eq": equip_command,
            "help": help_command,
            "h": help_command,
            "interact": interact_command,
            "i": interact_command,
            "inventory": inventory_command,
            "in": inventory_command,
            "look": look_command,
            "l": look_command,
            "mute": mute_command,
            "m": mute_command,
            "pickup": pickup_command,
            "p": pickup_command,
            "quit": quit_command,
            "q": quit_command,
            "say": say_command,
            "s": say_command,
            "shout": shout_command,
            "sh": shout_command,
            "status": status_command,
            "st": status_command,
            "whisper": whisper_command,
            "w": whisper_command,
			"who": who_command,
			"wh": who_command,
            "unequip": unequip_command,
            "un": unequip_command,
            "unmute": unmute_command,
            "u": unmute_command,
            }

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if user not in players: continue

        # Checks to see if the user has authenticated to the server.
        if players[user].authenticated:

            # if the player hasn't given their name yet, use this first command as their name
            if players[user].name == "unknown":

                # Allows the user to name their player and choose their class.
                create_player(*args)

            # each of the possible commands is handled below. Try adding new commands
            # to the game!

            else:
                # Check to determine if user input is within the command list
                # then execute that function
                try:
                    command_list[command](*args)
                    prompt_info(mud,user)
                # If the command is not within the list then execute the
                # unknown command function
                except KeyError:
                    unknown_command(*args)

        else:
            # since unauthenticated, this allows the user to enter the password
            login_check(mud,user,command)

def create_player(mud,user,command,params):
    """
    Since the player has yet to be named, this function will allow the player
    to name their character and 'eventually' choose their specific class.
    """
    # used to ensure a duplicate name is not chosen.
    duplicateName = False
    name_list = [command]
    if params:
        name_list.append(params)

    name_string = " ".join(name_list)

    # Iterate through all players to detect duplicate names
    for pid,pl in players.items():
        # Check if entered name is already in use
        if name_string == players[pid].name:

            duplicateName = True

        else:
            # check next player for duplicate name
            continue
    # Determine if duplicate name is true and tell the user to try again or
    # set the player's name and provide welcome info
    if duplicateName == True:
        # Display duplicate name message and reset duplicateName variable
        mud.send_message(user, "Sorry that name is already used.")
        duplicateName = False

    else:
        # Name the new player
        players[user].name = name_string

        # go through all the players in the game
        for pid,pl in players.items():
            # send each player a message to tell them about the new player
            mud.send_message(pid,"%s entered the game" % players[user].name)

        # send the new player a welcome message
        mud.send_message(user,"Welcome to the game, %s. Type '[h]elp' for a list of commands. Have fun!" % players[user].name)

        # send the new player the description of their current room
        mud.send_message(user,players[user].room.longDescription)

        # send player prompt to the user
        prompt_info(mud,user)

def enter_command(mud,user,command,params):
    """
    Handles the enter command. This allows the player to move from room to room
    """

    # store the exit name
    ex = params  #used to be params.lower()

    # store the player's current room
    rm = players[user].room

    # if the specified exit is found in the room's exits list
    if ex in rm.exits.keys():

        # go through all the players in the game
        for pid,pl in players.items():
            # if player is in the same room and isn't the player sending the command
            if players[pid].room.name == players[user].room.name and pid!=user:
                # send them a message telling them that the player left the room
                mud.send_message(pid,"%s left via exit '%s'" % (players[user].name,ex))

        # update the player's current room to the one the exit leads to
        players[user].room = rm.enter_room(ex)

        # go through all the players in the game
        for pid,pl in players.items():
            # if player is in the same (new) room and isn't the player sending the command
            if players[pid].room.name == players[user].room.name and pid!=user:
                # send them a message telling them that the player entered the room
                mud.send_message(pid,"%s arrived via exit '%s'" % (players[user].name,ex))

        # send the player a message telling them where they are now
        mud.send_message(user,"You arrive at '%s'" % players[user].room.name)
        mud.send_message(user,players[user].room.longDescription)

    # the specified exit wasn't found in the current room
    else:
        # send back an 'unknown exit' message
        mud.send_message(user, "Unknown exit '%s'" % ex)

def equip_command(mud,user,command,params):
    """
    Function that handles equiping items. Utilizes the character class method
    that checks if item exists in the inventory, equips item, removes from
    inventory, and then sends a message to the player based on if the item
    was able to be equipped.
    """

    if players[user].equip(params):   #the equip method returns a boolean
        mud.send_message(user, "Equipped " + params)
    else:
        mud.send_message(user, "Cannot equip " + params)

def unequip_command(mud,user,command,params):
    """
    Function that handles the unequip command. Utilizes the character class
    method to remove the item, restore the default attributes/equip, and places
    the item back into the inventory. Method returns a boolean to decide which
    message to send the user.
    """

    if players[user].unequip(params):   #returns a boolean based on success
        mud.send_message(user, "Unequipped " + params)
    else:
        mud.send_message(user, params + " is not equipped.")

def help_command(mud,user,command,params):
    """
    Provide the available commands within the help menu...
    """

    # send the player back the list of possible commands
    mud.send_message(user,"Commands:")
    mud.send_message(user,"  [e]nter <object>     - Moves through the exit specified, e.g. 'enter north'")
    mud.send_message(user,"  [un]/[eq]uip <item>  - Equips/Unequips an item, e.g. 'equip Dagger or unequip Dagger'")
    mud.send_message(user,"  [i]nteract <item>    - Further examines an item or player, e.g 'i [item]/[name]'")
    mud.send_message(user,"  [in]ventory          - Lists all of the items in your inventory, e.g. 'inventory'")
    mud.send_message(user,"  [l]ook               - Examines the surroundings, e.g. 'look'")
    mud.send_message(user,"  [u]n/[m]ute <player> - Mutes or unmutes a specific player, e.g. 'mute john' or 'unmute john'")
    mud.send_message(user,"  [p]ickup <item>      - Pickups an item, e.g. 'pickup Dagger.'")
    mud.send_message(user,"  [q]uit               - Closes the session to the MUD server.")
    mud.send_message(user,"  [s]ay <message>      - Says something out loud, e.g. 'say Hello'")
    mud.send_message(user,"  [sh]out <message>    - Shout something to all rooms, e.g. 'shout Hello!'")
    mud.send_message(user,"  [st]atus             - Displays a printout of the overall status and equipment of the user.")
    mud.send_message(user,"  [w]hisper            - Whisper a message to a single player, e.g. 'whisper john, Hello.'")
    mud.send_message(user,"  [wh]o                - Displays who and where each player are, e.g. 'player1 is in the Phoenix Tavern'")

def interact_command(mud,user,command,params):
    """
    Function that handles the interact command. The player can either interact
    with an item in the room or a character that is in the room. If they
    interact with a character then the class string will be presented to the
    player.
    """

    # store the player's current room
    rm = players[user].room

    # Iterate through items within the current room
    for item in rm.items:
        # Determine if the player is interacting with a valid object
        if item.name == params:
            # Send the description of the item
            mud.send_message(user, item.description)

    # Allows the player to get info on other players by interacting with them.
    for pid,pl in players.items():
        # Check through all players
        if players[pid].name == params:
            # Display the default character string
            mud.send_message(user, str(players[pid]))

def inventory_command(mud,user,command,params):
    """
    Function that handles the inventory command. Sends the list of items to the
    players console.
    """

    weapon = players[user].equipped_weapon.description
    armor = players[user].equipped_armor.description

    mud.send_message(user, ("Your weapon of choice: %s" % weapon))
    mud.send_message(user, ("You are wearing: %s" % armor))
    mud.send_message(user, "You have the following items:")
    for item in players[user].get_items():
        # print each item on a separate line
        mud.send_message(user, item)

def look_command(mud,user,command,params):
    """
    Function that handles the look command. Displays all of the available
    items in the area as well as the current players in the same room.
    """

    # store the player's current room
    rm = players[user].room

    # send the player back the description of their current room
    mud.send_message(user, rm.description)

    playersHere = []
    # go through every player in the game
    for pid,pl in players.items():
        # if they're in the same room as the player
        if players[pid].room.name == players[user].room.name:
            # add their name to the list
            playersHere.append(players[pid].name)

    roomItems = []
    # iterate through available items and append to list
    if rm.items:
        for item in rm.items:
            roomItems.append(item.displayName)
    else:
        roomItems.append("")

    # send player a message containing the list of players in the room
    mud.send_message(user, "Players here: %s" % ", ".join(playersHere))

    mud.send_message(user, "Items available: %s" % ", ".join(roomItems))

    # send player a message containing the list of exits from this room
    mud.send_message(user, "Exits are: %s" % ", ".join(rm.exits.keys()))

def mute_command(mud,user,command,params):
    """
    Function that handles the mute command. This will prevent room and world
    message broadcasts from being received by the player. The whisper command
    will not be effected.
    """
    # Check if a name was passed to the command
    if params:
        # iterate through all players to ensure the player name is valid
        for pid,next_player in players.items():

            if params.lower() == next_player.name.lower():

                # Check to ensure the player isn't already muted
                if params.lower() not in players[user].muted_players:
                    # Add the player to the list and inform the user
                    players[user].muted_players.append(params.lower())
                    mud.send_message(user, "%s has been muted." % params)

                    break

                else:
                    # Inform the user that the player is already muted
                    mud.send_message(user, "%s is already muted." % params)

                    break

        else:
            # Inform user that the player is not currently available to mute
            mud.send_message(user, "%s is not a valid player." % params)

    else:
        # if the mute command is performed with no parameter then provide
        # the user with a list of currently muted players
        mud.send_message(user,"Currently muted players: ")

        for muted_player in players[user].muted_players:

            mud.send_message(user, "-  %s" % muted_player)

def pickup_command(mud,user,command,params):
    """
    Function that handles the pickup command. The player can pickup an item
    based on the item's pickup_value. This item will be added to the player's
    inventory.
    """

    # store the player's current room
    rm = players[user].room

    # Iterate through items within the current room
    for item in rm.items:
        # Determine if the player is interacting with a valid object
        if item.name == params:
            # Iterate through items in inventory
            for onHand in players[user].inventory:
                # check if item currently exists in inventory
                if onHand.name == item.name:
                    # increment quantity and inform player
                    onHand.quantity = onHand.quantity + 1
                    rm.items.remove(item)
                    mud.send_message(user, "%s added to inventory" % item.displayName)

                    break
            else:
                # append new item into the inventory
                players[user].inventory.append(item)
                rm.items.remove(item)
                mud.send_message(user, "%s added to inventory" % item.displayName)


    # Allows the player to get info on other players by interacting with them.
    for pid,pl in players.items():
        # Check through all players
        if players[pid].name == params:
            # Display the default character string
            mud.send_message(user, "Hey no picking up on other players.")

def prompt_info(mud,user):
    """
    Function that handles the displaying of the player's prompt. This gathers
    the pertinent information from the character to build the display and
    sends it to the mud.send_prompt method:
    [health/max_health]name$
    """

    h = players[user].health
    m = players[user].max_health
    n =  players[user].name

    # creates the prompt and colors the username as yellow and current health as red
    prompt = "%s%s%s[%s%d%s/%d]%s$%s" % (color["yellow"],n,color["reset"],color["red"],h,color["reset"],m,color["yellow"],color["reset"])
    mud.send_prompt(user,prompt)

def unmute_command(mud,user,command,params):
    """
    Function that performs the unmuting of a player. This will ensure that the
    name provided is within the list of muted players and will then remove
    it from the list.
    """
    # Ensure a name is provided
    if params:
        # Try to remove the name or catch the exception to inform the user
        try:
            # remove the player from the muted list and inform the user
            players[user].muted_players.remove(params.lower())
            mud.send_message(user,"%s has been unmuted." % params)
        # player not in list exception
        except ValueError:
            # inform the user that the name provided was not in the list
            mud.send_message(user,"%s is not a muted player." % params)

def quit_command(mud,user,command,params):
    """
    Function use to handle the quit command. This can be used to further
    refine how we properly close out a user's session.
    """

    # Closes the player's connection
    mud.send_message(user,"Thanks for playing. Goodbye!")
    mud._handle_disconnect(user)

def say_command(mud,user,command,params):
    """
    Function that handles the say command. This will broadcast a message from
    the player to all the other players within the same room.
    """

    # go through every player in the game
    for pid,pl in players.items():
        # if they're in the same room as the player and not muted
        if pl.room.name == players[user].room.name and players[user].name.lower() not in pl.muted_players:
            # send them a message telling them what the player said
            mud.send_message(pid,"%s says: %s" % (players[user].name,params) )

def shout_command(mud,user,command,params):
    """
    Function that handles the shout command. This will broadcast a message to
    all players in every single room within the game. This obviously has
    potential for abuse. So a means to mute shouts will need to be developed.
    """

    # go through every player in the game
    for pid,pl in players.items():
        # if they are not muted
        if players[user].name.lower() not in pl.muted_players:
            # send message to everyone
            mud.send_message(pid,"%s shouts: %s" % (players[user].name,params))

def status_command(mud,user,command,params):
    """
    Function that handles the status command. This will display a huge listing
    of all of the stats and attributes for the player.
    """

    status_display = players[user].get_status()

    for line in status_display:

        mud.send_message(user, line)

def unknown_command(mud,user,command,params):
    """
    Handles the output provided when an unknown command is provided.
    """

    # send back an 'unknown command' message unless empty. Then just do a carriage return
    if command == "":

        prompt_info(mud,user)

    else:

        mud.send_message(user, "Unknown command '%s'" % command)
        mud.send_message(user, "Ensure to use lowercase commands.")

def who_command(mud,user,command,params):
	"""
	Displays all the players in the game and which room they are located.
	"""
	for pid,pl in players.items():
		mud.send_message(user,"%s is currently located: %s" % (players[pid].name,players[pid].room.name))

def whisper_command(mud,user,command,params):
    """
    Function that handles the whisper command. Allows the player to private
    message any other player so that it does not broadcast to all other players.
    """
    # Ensure that the command is trailed by a message
    try:
        # splits the received data between the intended target and their message
        name,whisperMessage = params.split(",",1)
        # ensure all characters are lowercase to help with comparison
        name = name.lower()

        # iterate through all players and set their names to lower case
        for pid,pl in players.items():
            testPlayer = players[pid].name.lower()

            # first test if player is whispering to themself
            if name == players[user].name.lower():
                # send a 'fun' message back to the user for whispering to themself
                mud.send_message(user,"%s whisper's to themself: %s *weirdo*" % (players[user].name,whisperMessage))
            # check to see if the player is whispering to an available character
            elif name == testPlayer:
                # ensure both parties see the whisper message
                mud.send_message(pid,"%s whispers to %s:%s" % (players[user].name,players[pid].name,whisperMessage))
                mud.send_message(user,"%s whispers to %s:%s" % (players[user].name,players[pid].name,whisperMessage))
    # if there was no message attached, inform the user
    except ValueError:

        mud.send_message(user, "Invalid whisper syntax, e.g [w]hisper 'name', message.")
