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

        if self.roomExists(direction):
            print "Room already exists."
            return

        dbmanager.dbmanobj.c.execute('insert into rooms (title, desc) values ("default title", "default desc")')
        
        new_room_id = dbmanager.dbmanobj.c.lastrowid

        # create the door to the room
        dbmanager.dbmanobj.c.execute('insert into doors (src_room_id, dest_room_id, dir) values (?,?,?)', (self.currentRoom.room_id, new_room_id, direction))

        #create the door from the new room back to this one
        dbmanager.dbmanobj.c.execute('insert into doors (src_room_id, dest_room_id, dir) values (?,?,?)', (new_room_id, self.currentRoom.room_id, opposite_dir[direction]))


        # refresh the current room
        self.currentRoom = Room(self.currentRoom.room_id)
        print "Room created to the " + direction

    def move(self, direction):

        if self.roomExists(direction):
            #print "Changing room to: " + str(self.currentRoom.exits[direction]
            self.currentRoom = Room(self.currentRoom.exits[direction])
        else:
            print "There are no exits in that direction."

    def roomExists(self, direction):
       
        dbmanager.dbmanobj.c.execute('select count(1) from doors where dir = ? and src_room_id = ?', (direction, self.currentRoom.room_id))
        room_count = dbmanager.dbmanobj.c.fetchone()[0]

        if room_count != 0:
            return True
        else:
            return False

