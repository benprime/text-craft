import dbmanager

class Room:
    #title = ""
    #desc = ""

    # constructor
    def __init__(self, room_id):
        
         # get the room from database
        dbmanager.dbmanobj.c.execute('select room_id, title, desc from rooms where room_id = ?', (room_id,))

        # there's probably a better way to do this

        row = dbmanager.dbmanobj.c.fetchone()

        self.room_id = row[0]
        self.title = row[1]
        self.desc = row[2]

        
        dbmanager.dbmanobj.c.execute('select dir, dest_room_id from doors where src_room_id = ?', (self.room_id,))

        self.exits = {}
        for row in dbmanager.dbmanobj.c:
            self.exits[row[0]] = row[1]

    def printDesc(self):
        print '\033[1;32m' + self.title + '\033[1;m'
        print '\033[1;30m' + self.desc + '\033[1;m'
        print 'Exits: ' + self.buildExitString()


    def buildExitString(self):
        if( len(self.exits) == 0 ):
            return "None."

        return ', '.join(self.exits.keys())

    def save(self):
        dbmanager.dbmanobj.c.execute('update rooms set title=?, desc=? where room_id=?', (self.title, self.desc, self.room_id))

