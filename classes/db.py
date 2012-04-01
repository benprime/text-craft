import os
import sqlite3

_conn = None


def conn():
    global _conn
    if not _conn:
        create = False

        if not os.path.exists('data.db'):
            create = True

        _conn = sqlite3.connect('data.db')
        c = _conn.cursor()

        if( create ):
            print "creating database data..."
            c.execute('create table rooms(room_id integer primary key, title text, desc text, x int, y int, z int, unique(x,y,z))')
            c.execute('insert into rooms (title, desc, x, y, z) values ("default room", "default desc", 0, 0, 0)')
            c.execute('create table doors( \
                         door_id integer primary key, \
                         src_room_id int, \
                         dest_room_id int, \
                         dir text, \
                         foreign key(src_room_id) references rooms(room_id), \
                         foreign key(dest_room_id) references rooms(room_id), \
                         unique(src_room_id, dir) \
                       )')

    return _conn



    


