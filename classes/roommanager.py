from room import Room
import db
import sys

opposite_dir = { 'north' : 'south',
                 'south' : 'north',
                 'east'  : 'west',
                 'west'  : 'east',
                 'northeast' : 'southwest',
                 'northwest' : 'southeast',
                 'southeast' : 'northwest',
                 'southwest' : 'northeast',
                 'up' : 'down',
                 'down' : 'up',
               }

class RoomManager:

    # constructor
    def __init__(self):
        self.current_room = Room(1)

    def create_room(self, direction):

        c = db.conn().cursor()
        
        # see if room already exists
        new_room_id = self.room_exists(direction)
       
        #if room does not exist, create it
        if new_room_id == 0:
            coords = self.get_coords_from_dir(direction)
            c.execute('insert into rooms (title, desc, x, y, z) values ("default title", "default desc", ?, ?, ?)', coords)
            new_room_id = c.lastrowid
        else:
            print "A room already exists at this map location, using existing room."


        if self.door_exists(direction):
            print "An exit already exists in that direction!"
            return

        # create the door to the room
        c.execute('insert into doors (src_room_id, dest_room_id, dir) values (?,?,?)', (self.current_room.room_id, new_room_id, direction))

        #create the door from the new room back to this one
        c.execute('insert into doors (src_room_id, dest_room_id, dir) values (?,?,?)', (new_room_id, self.current_room.room_id, opposite_dir[direction]))

        db.conn().commit()

        # refresh the current room
        self.current_room = Room(self.current_room.room_id)
        print "Room created to the " + direction

    
    def move(self, direction):

        if self.door_exists(direction):
            #print "Changing room to: " + str(self.current_room.exits[direction]
            self.current_room = Room(self.current_room.exits[direction])
        else:
            print "There are no exits in that direction."


    # this method is used when checking valid moves
    def door_exists(self, direction):
                
        c = db.conn().cursor()        
        c.execute('select count(1) from doors where src_room_id = ? and dir = ?', (self.current_room.room_id, direction))
        room_count = c.fetchone()[0]

        if room_count != 0:
            return True
        else:
            return False

    
    # returns true or false if a room exists based on the move direction
    # this method is used when creating rooms
    def room_exists(self, direction):

        coords = self.get_coords_from_dir(direction)
        c = db.conn().cursor()

        c.execute('select count(*) from rooms where x = ? and y = ? and z = ?', coords)
        count = c.fetchone()[0]

        if count != 0:
            c.execute('select room_id from rooms where x = ? and y = ? and z = ?', coords)
            room_id = c.fetchone()[0]
            return room_id
        else:
            return 0


    # Shortcut method for finding the coords based on move direction
    def get_coords_from_dir(self, direction):

        x = self.current_room.x
        y = self.current_room.y
        z = self.current_room.z

        if direction == "north":
            y += 1
        elif direction == "south":
            y -= 1
        elif direction == "east":
            x += 1
        elif direction == "west":
            x -= 1
        elif direction == "northwest":
            x -= 1
            y += 1
        elif direction == "northeast":
            x += 1
            y += 1
        elif direction == "southeast":
            x += 1
            y -= 1
        elif direction == "southwest":
            x -= 1
            y -= 1
        elif direction == "up":
            z += 1
        elif direction == "down":
            z -= 1

        else:
            print "Fatal error: Invalid move direction provided to room_exists : " + direction
            sys.exit(-1)

        return (x,y,z)



    def get_room_map(self, exit_list, current):
        
        # build line 1
        if 'northwest' in exit_list:
            line1c1 = '\\'
        else:
            line1c1 = ' '

        if 'north' in exit_list:
            line1c2 = '|'
        else:
            line1c2 = ' '

        if 'northeast' in exit_list:
            line1c3 = '/'
        else:
            line1c3 = ' '

        line1 = line1c1 + line1c2 + line1c3

        # build line 2
        if 'west' in exit_list:
            line2c1 = '-'
        else:
            line2c1 = ' '

        if current:
            line2c2 = '*'
        else:
            line2c2 = '#'

        if 'east' in exit_list:
            line2c3 = '-'
        else:
            line2c3 = ' '

        line2 = line2c1 + line2c2 + line2c3

        # build line 3
        if 'southwest' in exit_list:
            line3c1 = "/"
        else:
            line3c1 = ' '

        if 'south' in exit_list:
            line3c2 = '|'
        else:
            line3c2 = ' '

        if 'southeast' in exit_list:
            line3c3 = '\\'
        else:
            line3c3 = ' '

        line3 = line3c1 + line3c2 + line3c3

        return (line1, line2, line3)

