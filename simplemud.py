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

# standard library imports
import time
import os
import sys

# add the mud_py data directory to the python path variable
mud_dir = os.path.join(os.getcwd() + '/data')
sys.path.append(mud_dir)

# local imports
from mudserver import MudServer
from gamefunctions import new_players_check
from gamefunctions import disconnected_players_check
from gamefunctions import process_commands



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
    new_players_check(mud)
    disconnected_players_check(mud)
    process_commands(mud)
