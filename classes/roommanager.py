from room import Room
import dbmanager

opposite_dir = { 'north' : 'south',
                 'south' : 'north',
                 'east'  : 'west',
                 'west'  : 'east',
                 'northeast' : 'southwest',
                 'northwest' : 'southeast',
                 'southeast' : 'northwest',
                 'southwest' : 'northeast',
               }

class RoomManager:

    # constructor
    def __init__(self):
        self.currentRoom = Room(1)

    def createRoom(self, direction):

        # see if room already exists
        new_room_id = self.roomExists(direction)
       
        #if room does not exist, create it
        if new_room_id == 0:
            coords = self.getCoordsFromDir(direction)
            dbmanager.dbmanobj.c.execute('insert into rooms (title, desc, x, y, z) values ("default title", "default desc", ?, ?, ?)', coords)
            new_room_id = dbmanager.dbmanobj.c.lastrowid
        else:
            print "A room already exists at this map location, using existing room."


        if self.doorExists(direction):
            print "An exit already exists in that direction!"
            return

        # create the door to the room
        dbmanager.dbmanobj.c.execute('insert into doors (src_room_id, dest_room_id, dir) values (?,?,?)', (self.currentRoom.room_id, new_room_id, direction))

        #create the door from the new room back to this one
        dbmanager.dbmanobj.c.execute('insert into doors (src_room_id, dest_room_id, dir) values (?,?,?)', (new_room_id, self.currentRoom.room_id, opposite_dir[direction]))

        dbmanager.dbmanobj.conn.commit()

        # refresh the current room
        self.currentRoom = Room(self.currentRoom.room_id)
        print "Room created to the " + direction

    
    def move(self, direction):

        if self.doorExists(direction):
            #print "Changing room to: " + str(self.currentRoom.exits[direction]
            self.currentRoom = Room(self.currentRoom.exits[direction])
        else:
            print "There are no exits in that direction."


    # this method is used when checking valid moves
    def doorExists(self, direction):
                
        dbmanager.dbmanobj.c.execute('select count(1) from doors where src_room_id = ? and dir = ?', (self.currentRoom.room_id, direction))
        room_count = dbmanager.dbmanobj.c.fetchone()[0]

        if room_count != 0:
            return True
        else:
            return False

    
    # returns true or false if a room exists based on the move direction
    # this method is used when creating rooms
    def roomExists(self, direction):

        coords = self.getCoordsFromDir(direction)

        dbmanager.dbmanobj.c.execute('select count(*) from rooms where x = ? and y = ? and z = ?', coords)
        count = dbmanager.dbmanobj.c.fetchone()[0]

        if count != 0:
            dbmanager.dbmanobj.c.execute('select room_id from rooms where x = ? and y = ? and z = ?', coords)
            room_id = dbmanager.dbmanobj.c.fetchone()[0]
            return room_id
        else:
            return 0


    # Shortcut method for finding the coords based on move direction
    def getCoordsFromDir(self, direction):

        x = self.currentRoom.x
        y = self.currentRoom.y
        z = self.currentRoom.z

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
        else:
            print "Fatal error: Invalid move direction provided to roomExists : " + direction
            sys.exit(-1)

        return (x,y,z)
        
