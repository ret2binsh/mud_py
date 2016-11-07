"""
A simple Multi-User Dungeon (MUD) game. Players can talk to each other, examine
their surroundings and move between rooms.

Some ideas for things to try adding:
    * More rooms to explore!
    * An 'emote' command e.g. 'emote laughs out loud' -> 'Mark laughs out loud'
    * A 'whisper' command for talking to individual players
    * A 'shout' command for yelling to players in all rooms
    * Items to look at in rooms e.g. 'look fireplace' -> 'You see a roaring, glowing fire'
    * Items to pick up e.g. 'take rock' -> 'You pick up the rock'
    * Monsters to fight
    * Loot to collect
    * Saving players accounts between sessions
    * A password login
    * A shop from which to buy items

author: Mark Frimston - mfrimston@gmail.com
"""

import time
import hashlib

# import  available rooms from the rooms dependency file
from rooms import rooms

# import the MUD server class
from mudserver import MudServer

# stores the players in the game
players = {}
duplicateName = False

# start the server
mud = MudServer()

# main game loop. We loop forever (i.e. until the program is terminated)
while True:

	# pause for 1/5 of a second on each loop, so that we don't constantly
	# use 100% CPU time
    time.sleep(0.2)

    # 'update' must be called in the loop to keep the game running and give
    # us up-to-date information
    mud.update()

    # go through any newly connected players
    for id in mud.get_new_players():

        # add the new player to the dictionary, noting that they've not been
        # named yet.
        # The dictionary key is the player's id number. Start them off in the
        # 'Tavern' room.
        # Try adding more player stats - level, gold, inventory, etc
        players[id] = {
            "name": "unknown",
            "room": "Tavern",
            "authenticated": False,
            "afk_status": False,
        }

        # send the new player the game banner
        banner = open('banner.txt', 'r')
        mud.send_message(id, banner.read())
        banner.close()
        # send the new player a prompt for their name
        mud.send_message(id,"Please enter the login password: ")


    # go through any recently disconnected players
    for id in mud.get_disconnected_players():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players: continue

        # go through all the players in the game
        for pid,pl in players.items():
            # send each player a message to tell them about the diconnected player
            mud.send_message(pid,"%s quit the game" % players[id]["name"])

        # remove the player's entry in the player dictionary
        del(players[id])


    # go through any new commands sent from players
    for id,command,params in mud.get_commands():

        # Checks to see if the user has authenticated to the server.
        if players[id]["authenticated"]:

            # if for any reason the player isn't in the player map, skip them and
            # move on to the next one
            if id not in players: continue

            # if the player hasn't given their name yet, use this first command as their name
            if players[id]["name"] == "unknown":

                # Iterate through all players to detect duplicate names
                for pid,pl in players.items():
                    # Check if entered name is already in use
                    if command + ' ' + params == players[pid]["name"]:

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
                    players[id]["name"] = command + ' ' + params

                    # go through all the players in the game
                    for pid,pl in players.items():
                        # send each player a message to tell them about the new player
                        mud.send_message(pid,"%s entered the game" % players[id]["name"])

                    # send the new player a welcome message
                    mud.send_message(id,"Welcome to the game, %s. Type '[h]elp' for a list of commands. Have fun!" % players[id]["name"])

                    # send the new player the description of their current room
                    mud.send_message(id,rooms[players[id]["room"]]["description"])

            # each of the possible commands is handled below. Try adding new commands
            # to the game!

            # 'help' command
            elif command == "help" or command == "h":

                # send the player back the list of possible commands
                mud.send_message(id,"Commands:")
                mud.send_message(id,"  [s]ay <message>  - Says something out loud, e.g. 'say Hello'")
                mud.send_message(id,"  [sh]out <message>  - Shout something to all rooms, e.g. 'shout Hello!'")
                mud.send_message(id,"  [w]hisper          -Whisper a message to a single player, e.g. 'whisper john, Hello.'")
                mud.send_message(id,"  [l]ook           - Examines the surroundings, e.g. 'look'")
                mud.send_message(id,"  [i]nteract <item>  -Further examines an item")
                mud.send_message(id,"  [e]nter <exit>      - Moves through the exit specified, e.g. 'enter outside'")
                mud.send_message(id,"  [q]uit            - Closes the session to the MUD server.")

            # 'say' command
            elif command == "say" or command == "s":

                # go through every player in the game
                for pid,pl in players.items():
                    # if they're in the same room as the player
                    if players[pid]["room"] == players[id]["room"]:
                        # send them a message telling them what the player said
                        mud.send_message(pid,"%s says: %s" % (players[id]["name"],params) )

            elif command == "shout" or command == "sh":

                # go through every player in the game
                for pid,pl in players.items():
                    # send message to everyone
                    mud.send_message(pid,"%s shouts: %s" % (players[id]["name"],params) )

            elif command == "whisper" or command == "w":

                try:

                    name,whisperMessage = params.split(",",1)
                    name = name.lower()

                    for pid,pl in players.items():
                        testPlayer = players[pid]["name"].lower()

                        if name.split() == testPlayer.split():

                            mud.send_message(pid,"%s whispers to %s:%s" % (players[id]["name"],players[pid]["name"],whisperMessage))
                            mud.send_message(id,"%s whispers to %s:%s" % (players[id]["name"],players[pid]["name"],whisperMessage))

                except ValueError:

                    mud.send_message(id, "Invalid whisper syntax, e.g [w]hisper 'name', message.")

            # 'look' command
            elif command == "look" or command == "l":

                # store the player's current room
                rm = rooms[players[id]["room"]]

                # send the player back the description of their current room
                mud.send_message(id, rm["description"])

                playershere = []
                # go through every player in the game
                for pid,pl in players.items():
                    # if they're in the same room as the player
                    if players[pid]["room"] == players[id]["room"]:
                        # add their name to the list
                        playershere.append(players[pid]["name"])

                # send player a message containing the list of players in the room
                mud.send_message(id, "Players here: %s" % ", ".join(playershere))

                mud.send_message(id, "Items available: %s" % ", ".join(rm["items"]))

                # send player a message containing the list of exits from this room
                mud.send_message(id, "Exits are: %s" % ", ".join(rm["exits"]))

            elif command == "interact" or command == "i":

                # store the player's current room
                rm = rooms[players[id]["room"]]

                # Iterate through items within the current room
                for item in rm["items"]:
                    # Determine if the player is interacting with a valid object
                    if item == params:
                        # Send the description of the item
                        mud.send_message(id, rm["items"][item])

            # 'go' command
            elif command == "enter" or command == "e":

                # store the exit name
                ex = params.lower()

                # store the player's current room
                rm = rooms[players[id]["room"]]

                # if the specified exit is found in the room's exits list
                if ex in rm["exits"]:

                    # go through all the players in the game
                    for pid,pl in players.items():
                        # if player is in the same room and isn't the player sending the command
                        if players[pid]["room"] == players[id]["room"] and pid!=id:
                            # send them a message telling them that the player left the room
                            mud.send_message(pid,"%s left via exit '%s'" % (players[id]["name"],ex))

                    # update the player's current room to the one the exit leads to
                    players[id]["room"] = rm["exits"][ex]
                    rm = rooms[players[id]["room"]]

                    # go through all the players in the game
                    for pid,pl in players.items():
                        # if player is in the same (new) room and isn't the player sending the command
                        if players[pid]["room"] == players[id]["room"] and pid!=id:
                            # send them a message telling them that the player entered the room
                            mud.send_message(pid,"%s arrived via exit '%s'" % (players[id]["name"],ex))

                    # send the player a message telling them where they are now
                    mud.send_message(id,"You arrive at '%s'" % players[id]["room"])

                # the specified exit wasn't found in the current room
                else:
                    # send back an 'unknown exit' message
                    mud.send_message(id, "Unknown exit '%s'" % ex)

            elif command == "quit" or command == "q":

                # Closes the player's connection
                mud.send_message(id,"Thanks for playing. Goodbye!")
                mud._handle_disconnect(id)

            # some other, unrecognised command
            else:
                # send back an 'unknown command' message
                mud.send_message(id, "Unknown command '%s'" % command)
                mud.send_message(id, "Ensure to use lowercase commands.")

        else:

            # Get server hash from pass file.
            file_conn = open('pass', 'r')
            serverSecret = file_conn.readline()
            file_conn.close()

            # Compare user provide password against the stored hash
            hashResult = hashlib.sha224(command).hexdigest()
            if hashResult != serverSecret:
                mud.send_message(id, "Sorry, you provided an incorrect password.")
            else:
                players[id]["authenticated"] = mud.authentication_status(id,True)
                mud.send_message(id, "Welcome!")
                mud.send_message(id, "What is your name?")
