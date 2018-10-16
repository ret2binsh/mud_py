import hashlib

from character import Warrior
from rooms import *
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

def login_check(mud,id,command):
    """
    Reads the server password hash file and compares the user provided
    password against it. The user's authentication status will be set to True
    once the correct password is entered.
    """

    # Get server hash from pass file.
    file_conn = open('pass', 'r')
    serverSecret = file_conn.readline()
    file_conn.close()

    # Compare user provide password against the stored hash
    hashResult = hashlib.sha224(command).hexdigest()
    if hashResult != serverSecret:
        mud.send_message(id, "Sorry, you provided an incorrect password.")
    else:
        players[id].authenticated = mud.authentication_status(id,True)
        mud.send_message(id, "Welcome!")
        mud.send_message(id, "What is your name?")

def new_players_check(mud):
    """
    Checks to see if there are new players that have joined the server.
    Displays a banner and adds the user to the list of players.
    """

    # go through any newly connected players
    for id in mud.get_new_players():

        # add the new player to the dictionary using the Character class.
        # all default attributes are loaded and stored within the Character
        # object that can be accessed using the id key.
        players[id] = Warrior()

        # send the new player the game banner
        for line in bannerText:

            mud.send_message(id, line)

        # send the new player a prompt for the server password
        mud.send_message(id,"%sPlease enter the login password:%s" % (color["red"],color["reset"]))

def disconnected_players_check(mud):
    """
    Checks for disconnected players. If there are any then they are removed
    from the players dictionary.
    """

    # go through any recently disconnected players
    for id in mud.get_disconnected_players():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players: continue

        # go through all the players in the game
        for pid,pl in players.items():
            # send each player a message to tell them about the diconnected player
            mud.send_message(pid,"%s quit the game" % players[id].name)

        # remove the player's entry in the player dictionary
        del(players[id])

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
    for id,command,params in mud.get_commands():

        # arguments list used for the command list
        args = [mud,id,command,params]

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
            "whisper": whisper_command,
            "w": whisper_command,
            "unmute": unmute_command,
            "un": unmute_command,
            }

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players: continue

        # Checks to see if the user has authenticated to the server.
        if players[id].authenticated:

            # if the player hasn't given their name yet, use this first command as their name
            if players[id].name == "unknown":

                # Allows the user to name their player and choose their class.
                create_player(*args)

            # each of the possible commands is handled below. Try adding new commands
            # to the game!

            else:
                # Check to determine if user input is within the command list
                # then execute that function
                try:
                    command_list[command](*args)
                    prompt_info(mud,id)
                # If the command is not within the list then execute the
                # unknown command function
                except KeyError:
                    unknown_command(*args)

        else:
            # since unauthenticated, this allows the user to enter the password
            login_check(mud,id,command)

def create_player(mud,id,command,params):
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
        mud.send_message(id, "Sorry that name is already used.")
        duplicateName = False

    else:
        # Name the new player
        players[id].name = name_string

        # go through all the players in the game
        for pid,pl in players.items():
            # send each player a message to tell them about the new player
            mud.send_message(pid,"%s entered the game" % players[id].name)

        # send the new player a welcome message
        mud.send_message(id,"Welcome to the game, %s. Type '[h]elp' for a list of commands. Have fun!" % players[id].name)

        # send the new player the description of their current room
        mud.send_message(id,players[id].room.longDescription)

        # send player prompt to the user
        prompt_info(mud,id)

def enter_command(mud,id,command,params):
    """
    Handles the enter command. This allows the player to move from room to room
    """

    # store the exit name
    ex = params  #used to be params.lower()

    # store the player's current room
    rm = players[id].room

    # if the specified exit is found in the room's exits list
    if ex in rm.exits:

        # go through all the players in the game
        for pid,pl in players.items():
            # if player is in the same room and isn't the player sending the command
            if players[pid].room.name == players[id].room.name and pid!=id:
                # send them a message telling them that the player left the room
                mud.send_message(pid,"%s left via exit '%s'" % (players[id].name,ex))

        # update the player's current room to the one the exit leads to
        players[id].room = roomExits[ex]
        #rm = players[id].room

        # go through all the players in the game
        for pid,pl in players.items():
            # if player is in the same (new) room and isn't the player sending the command
            if players[pid].room.name == players[id].room.name and pid!=id:
                # send them a message telling them that the player entered the room
                mud.send_message(pid,"%s arrived via exit '%s'" % (players[id].name,ex))

        # send the player a message telling them where they are now
        mud.send_message(id,"You arrive at '%s'" % players[id].room.name)
        mud.send_message(id,players[id].room.longDescription)

    # the specified exit wasn't found in the current room
    else:
        # send back an 'unknown exit' message
        mud.send_message(id, "Unknown exit '%s'" % ex)

def equip_command(mud,id,command,params):
    """
    Function that handles equiping items. Will check the items attributes
    to determine whether it can be equipped and if it is a weapon or armor.
    """

    for item in players[id].inventory:
        # iterate through the inventory and then check if the typed item
        # matches prior to determining if it can be equipped.
        if item.name == params:

            if item.equip:
                # equip the item and then send the player a message
                players[id].equip(item)
                mud.send_message(id, "Equipped " + item.name)
                break
            else:
                # if the item is not equippable inform the player
                mud.send_message(id, "Cannot equip " + item.name)
                break

    else:
        # inform the player if the item typed in isn't in the inventory
        mud.send_message(id, "There's no " + params + " to equip.")



def help_command(mud,id,command,params):
    """
    Provide the available commands within the help menu...
    """

    # send the player back the list of possible commands
    mud.send_message(id,"Commands:")
    mud.send_message(id,"  [e]nter <object>     - Moves through the exit specified, e.g. 'enter outside'")
    mud.send_message(id,"  [i]nteract <item>    - Further examines an item or player, e.g 'i [item]/[name]'")
    mud.send_message(id,"  [in]ventory          - Lists all of the items in your inventory, e.g. 'inventory'")
    mud.send_message(id,"  [l]ook               - Examines the surroundings, e.g. 'look'")
    mud.send_message(id,"  [un]/[m]ute <player> - Mutes or unmutes a specific player, e.g. 'mute john' or 'unmute john'")
    mud.send_message(id,"  [p]ickup <item>      - Pickups an item, e.g. 'pickup Dagger.'")
    mud.send_message(id,"  [q]uit               - Closes the session to the MUD server.")
    mud.send_message(id,"  [s]ay <message>      - Says something out loud, e.g. 'say Hello'")
    mud.send_message(id,"  [sh]out <message>    - Shout something to all rooms, e.g. 'shout Hello!'")
    mud.send_message(id,"  [w]hisper            - Whisper a message to a single player, e.g. 'whisper john, Hello.'")

def interact_command(mud,id,command,params):
    """
    Function that handles the interact command. The player can either interact
    with an item in the room or a character that is in the room. If they
    interact with a character then the class string will be presented to the
    player.
    """

    # store the player's current room
    rm = players[id].room

    # Iterate through items within the current room
    for item in rm.items:
        # Determine if the player is interacting with a valid object
        if item.name == params:
            # Send the description of the item
            mud.send_message(id, item.description)

    # Allows the player to get info on other players by interacting with them.
    for pid,pl in players.items():
        # Check through all players
        if players[pid].name == params:
            # Display the default character string
            mud.send_message(id, str(players[pid]))

def inventory_command(mud,id,command,params):
    """
    Function that handles the inventory command. Sends the list of items to the
    players console.
    """

    weapon = players[id].equipped_weapon.description
    armor = players[id].equipped_armor.description

    mud.send_message(id, ("Your weapon of choice: %s" % weapon))
    mud.send_message(id, ("You are wearing: %s" % armor))
    mud.send_message(id, "You have the following items:")
    for item in players[id].get_items():
        # print each item on a separate line
        mud.send_message(id, item)

def look_command(mud,id,command,params):
    """
    Function that handles the look command. Displays all of the available
    items in the area as well as the current players in the same room.
    """

    # store the player's current room
    rm = players[id].room

    # send the player back the description of their current room
    mud.send_message(id, rm.description)

    playersHere = []
    # go through every player in the game
    for pid,pl in players.items():
        # if they're in the same room as the player
        if players[pid].room.name == players[id].room.name:
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
    mud.send_message(id, "Players here: %s" % ", ".join(playersHere))

    mud.send_message(id, "Items available: %s" % ", ".join(roomItems))

    # send player a message containing the list of exits from this room
    mud.send_message(id, "Exits are: %s" % ", ".join(rm.exits))

def mute_command(mud,id,command,params):
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
                if params.lower() not in players[id].muted_players:
                    # Add the player to the list and inform the user
                    players[id].muted_players.append(params.lower())
                    mud.send_message(id, "%s has been muted." % params)

                    break

                else:
                    # Inform the user that the player is already muted
                    mud.send_message(id, "%s is already muted." % params)

                    break

        else:
            # Inform user that the player is not currently available to mute
            mud.send_message(id, "%s is not a valid player." % params)

    else:
        # if the mute command is performed with no parameter then provide
        # the user with a list of currently muted players
        mud.send_message(id,"Currently muted players: ")

        for muted_player in players[id].muted_players:

            mud.send_message(id, "-  %s" % muted_player)

def pickup_command(mud,id,command,params):
    """
    Function that handles the pickup command. The player can pickup an item
    based on the item's pickup_value. This item will be added to the player's
    inventory.
    """

    # store the player's current room
    rm = players[id].room

    # Iterate through items within the current room
    for item in rm.items:
        # Determine if the player is interacting with a valid object
        if item.name == params:
            # Iterate through items in inventory
            for onHand in players[id].inventory:
                # check if item currently exists in inventory
                if onHand.name == item.name:
                    # increment quantity and inform player
                    onHand.quantity = onHand.quantity + 1
                    mud.send_message(id, "%s added to inventory" % item.displayName)
                    break
            else:
                # append new item into the inventory
                players[id].inventory.append(item)
                mud.send_message(id, "%s added to inventory" % item.displayName)


    # Allows the player to get info on other players by interacting with them.
    for pid,pl in players.items():
        # Check through all players
        if players[pid].name == params:
            # Display the default character string
            mud.send_message(id, "Hey no picking up on other players.")

def prompt_info(mud,id):
    """
    Function that handles the displaying of the player's prompt. This gathers
    the pertinent information from the character to build the display and
    sends it to the mud.send_prompt method:
    [health/max_health]name$
    """

    h = players[id].health
    m = players[id].max_health
    n =  players[id].name

    # creates the prompt and colors the username as yellow and current health as red
    prompt = "%s%s%s[%s%d%s/%d]%s$%s" % (color["yellow"],n,color["reset"],color["red"],h,color["reset"],m,color["yellow"],color["reset"])
    mud.send_prompt(id,prompt)

def unmute_command(mud,id,command,params):
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
            players[id].muted_players.remove(params.lower())
            mud.send_message(id,"%s has been unmuted." % params)
        # player not in list exception
        except ValueError:
            # inform the user that the name provided was not in the list
            mud.send_message(id,"%s is not a muted player." % params)

def quit_command(mud,id,command,params):
    """
    Function use to handle the quit command. This can be used to further
    refine how we properly close out a user's session.
    """

    # Closes the player's connection
    mud.send_message(id,"Thanks for playing. Goodbye!")
    mud._handle_disconnect(id)

def say_command(mud,id,command,params):
    """
    Function that handles the say command. This will broadcast a message from
    the player to all the other players within the same room.
    """

    # go through every player in the game
    for pid,pl in players.items():
        # if they're in the same room as the player and not muted
        if pl.room.name == players[id].room.name and players[id].name.lower() not in pl.muted_players:
            # send them a message telling them what the player said
            mud.send_message(pid,"%s says: %s" % (players[id].name,params) )

def shout_command(mud,id,command,params):
    """
    Function that handles the shout command. This will broadcast a message to
    all players in every single room within the game. This obviously has
    potential for abuse. So a means to mute shouts will need to be developed.
    """

    # go through every player in the game
    for pid,pl in players.items():
        # if they are not muted
        if players[id].name.lower() not in pl.muted_players:
            # send message to everyone
            mud.send_message(pid,"%s shouts: %s" % (players[id].name,params))

def unknown_command(mud,id,command,params):
    """
    Handles the output provided when an unknown command is provided.
    """

    # send back an 'unknown command' message unless empty. Then just do a carriage return
    if command == "":

        prompt_info(mud,id)

    else:

        mud.send_message(id, "Unknown command '%s'" % command)
        mud.send_message(id, "Ensure to use lowercase commands.")

def whisper_command(mud,id,command,params):
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
            if name == players[id].name.lower():
                # send a 'fun' message back to the user for whispering to themself
                mud.send_message(id,"%s whisper's to themself: %s *weirdo*" % (players[id].name,whisperMessage))
            # check to see if the player is whispering to an available character
            elif name == testPlayer:
                # ensure both parties see the whisper message
                mud.send_message(pid,"%s whispers to %s:%s" % (players[id].name,players[pid].name,whisperMessage))
                mud.send_message(id,"%s whispers to %s:%s" % (players[id].name,players[pid].name,whisperMessage))
    # if there was no message attached, inform the user
    except ValueError:

        mud.send_message(id, "Invalid whisper syntax, e.g [w]hisper 'name', message.")
