#!/usr/bin/python -tt

from classes.roommanager import RoomManager
from classes.dbmanager import DBManager

import re

roomMan = RoomManager()

movement_actions = ("north", "south", "east", "west", "northwest", "northeast", "southeast", "southwest")

def debug():
    print "Current room_id: " + str(roomMan.currentRoom.room_id)
    print "Exits: " + str(roomMan.currentRoom.exits)

def auto_complete(action_string):
  
    #special case for direction short hand
    if(action_string == 'n'): return 'north'
    if(action_string == 'w'): return 'west'
    if(action_string == 'e'): return 'east'
    if(action_string == 's'): return 'south'
    if(action_string == 'nw'): return 'northwest'
    if(action_string == 'ne'): return 'northeast'
    if(action_string == 'se'): return 'southeast'
    if(action_string == 'sw'): return 'southwest'

    # if the action is anything else, we'll autocomplete it
    # based on the action word list here
    return action_string


while(True):

    print
    roomMan.currentRoom.printDesc()
    command = raw_input("> ")

    #create tuple of input string, split on non-word characters
    commands = re.split('\W+', command)

    if len(commands) > 0:
        action = auto_complete(commands[0])
        if len(commands) > 1:
            noun = commands[1]
        else:
            noun = ""

        if len(commands) > 2:
            match = re.search(r'\w+\W+\w+\W+(.+)', command)
            value = match.group(1)
        else:
            value = ""
    else:
        action = ""
        noun = ""
        value = ""




    #match = re.search(r'(\w+)\s+(\w+)\s+(\w+)', command) 
    #action = match.group(1)
    #noun = match.group(2)
    #value = match.group(3)

    if action == "exit" or action == "quit":
        sys.exit(0)
    elif action == "help":
        print "You don't need any help. ;)"

    # movement commands
    elif action in movement_actions:
        roomMan.move(action)
    elif action == "debug":
        debug()

    # admin commands
    elif action == "set":
        if noun == "title":
            if value != "":
                roomMan.currentRoom.title = value
                roomMan.currentRoom.save()
                print "title set to: " + value
            else:
                print "title must have a value"
        elif noun == "desc":
            if value != "":
                roomMan.currentRoom.desc = value
                roomMan.currentRoom.save()
                print "desc set to: " + value
            else:
                print "desc must have a value"
        else:
            print "invalid set command"
    elif action == "create":
        if noun == "room":
            if value == "n" or value == "north":
                roomMan.createRoom("north")
            elif value == "s" or value == "south":
                roomMan.createRoom("south")
            elif value == "e" or value == "east":
                roomMan.createRoom("east")
            elif value == "w" or value == "west":
                roomMan.createRoom("west")
            elif value == "nw" or value == "northwest":
                roomMan.createRoom("northwest")
            elif value == "ne" or value == "northeast":
                roomMan.createRoom("northeast")
            elif value == "sw" or value == "southwest":
                roomMan.createRoom("southwest")
            elif value == "se" or value == "southeast":
                roomMan.createRoom("southeast")
            else:
                print "Usage goes here"


        else:
            print "Usage examples: create room north"
            print "                create room southwest"
            print "                create room n"
            print "                create room sw"


    elif action != "":
        print "I'm not sure how to do that."

        


