import os
import sqlite3

class DBManager:


    def __init__(self):
        create = False

        if not os.path.exists('data.db'):
            create = True

        con = sqlite3.connect('data.db')
        self.c = con.cursor()

        if( create ):
            print "creating database data..."
            self.c.execute('create table rooms(room_id integer primary key, title text, desc text)')
            self.c.execute('insert into rooms (title, desc) values ("default room", "default desc")')
            self.c.execute('create table doors(door_id integer primary key, src_room_id int, dest_room_id int, dir text, foreign key(src_room_id) references rooms(room_id), foreign key(dest_room_id) references rooms(room_id), unique(src_room_id, dir))')

            

dbmanobj = DBManager()



    


