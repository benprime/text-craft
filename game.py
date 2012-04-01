#!/usr/bin/python -tt

from classes.roommanager import RoomManager
import classes.db

import sys
import re
import math

roomMan = RoomManager()

movement_actions = ("north", "south", "east", "west", "northwest", "northeast", "southeast", "southwest", "up", "down")

def debug():
    print "Current room_id: " + str(roomMan.current_room.room_id)
    print "Exits: " + str(roomMan.current_room.exits)

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
    if(action_string == 'u'): return 'up'
    if(action_string == 'd'): return 'down'

    # if the action is anything else, we'll autocomplete it
    # based on the action word list here
    # TODO: Add actions to this list as we continue to create
    #       the game.
    return action_string


# Method to draw an ascii map of the current area
def draw_map():
    
    # set the bounds of the map (3 square radius around current room)
    x_min = roomMan.current_room.x - 3
    x_max = roomMan.current_room.x + 3
    y_min = roomMan.current_room.y - 3
    y_max = roomMan.current_room.y + 3

 
    sql = 'select rooms.room_id, doors.dir, rooms.x, rooms.y from doors \
       inner join rooms on (doors.src_room_id = rooms.room_id) \
       where rooms.z = ? \
       and rooms.x between ? and ? \
       and rooms.y between ? and ? \
       order by rooms.room_id, rooms.y desc, rooms.x'

    c = classes.db.conn().cursor()
    db_rows = c.execute(sql, (roomMan.current_room.z, x_min, x_max, y_min, y_max))

    room_data = {}

    # loop through results and build a dictionary of exit value lists
    for row in db_rows:

        # key in the form of "x,y"
        key = str(row[2]) + ',' + str(row[3])
 
        if( key in room_data ):
            room_data[key].append(row[1])
        else:
            room_data[key] = [row[1]]

    

    # print a title for the map
    if roomMan.current_room.z >= 0:
        print "Map of floor " + str(roomMan.current_room.z+1)
    else:
        print "Map of basement level " + str(math.fabs(roomMan.current_room.z))

    for y in reversed(range(y_min, y_max)):
        
        line1 = ''
        line2 = ''
        line3 = ''

        for x in range(x_min, x_max):
            key = str(x) + ',' + str(y)

            if key in room_data:
                is_current_room = (x == roomMan.current_room.x and y == roomMan.current_room.y)
                room_map = roomMan.get_room_map(room_data[key], is_current_room)
            else:
                room_map = ('   ', '   ', '   ')
            
            line1 += room_map[0]
            line2 += room_map[1]
            line3 += room_map[2]

        print line1
        print line2
        print line3


    print " # = room"
    print " * = You are here"

while(True):

    print
    roomMan.current_room.print_desc()
    command = raw_input("> ")

    #create tuple of input string, split on non-word characters
    commands = re.split('\W+', command)

    #convention:
    # first word - action
    # second word - noun
    # remaining words - value
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
        print "Create your own text game map v1.0"
        print "  By Ben Smith, March 2012"
        print
        print "commands:"
        print "  create room <direction> - creates a room in the specified direction."
        print "      Valid directions: n, s, e, w, nw, sw, ne, se, u, d"
        print "  set title <title> - sets current room title."
        print "  set desc <desc> - sets the current room description."
        print "  map - displays a map of your current area."
        print "  debug - display room_id (database id) of your current room."
        print "  quit/exit - exits the script."

    # movement commands
    elif action in movement_actions:
        roomMan.move(action)
    elif action == "debug":
        debug()

    # admin commands
    elif action == "set":
        if noun == "title":
            if value != "":
                roomMan.current_room.title = value
                roomMan.current_room.save()
                print "title set to: " + value
            else:
                print "title must have a value"
        elif noun == "desc":
            if value != "":
                roomMan.current_room.desc = value
                roomMan.current_room.save()
                print "desc set to: " + value
            else:
                print "desc must have a value"
        else:
            print "invalid set command"
    elif action == "create":
        if noun == "room":
            if value == "n" or value == "north":
                roomMan.create_room("north")
            elif value == "s" or value == "south":
                roomMan.create_room("south")
            elif value == "e" or value == "east":
                roomMan.create_room("east")
            elif value == "w" or value == "west":
                roomMan.create_room("west")
            elif value == "nw" or value == "northwest":
                roomMan.create_room("northwest")
            elif value == "ne" or value == "northeast":
                roomMan.create_room("northeast")
            elif value == "sw" or value == "southwest":
                roomMan.create_room("southwest")
            elif value == "se" or value == "southeast":
                roomMan.create_room("southeast")
            elif value == "u" or value == "up":
                roomMan.create_room("up")
            elif value == "d" or value == "down":
                roomMan.create_room("down")
            else:
                print "Invalid create command."
        else:
            print "Invalid create command."


    elif action == "map":
        draw_map()

    elif action != "":
        print "I'm not sure how to do that."

        


