# world.py
import sqlite3
import io
from PIL import Image
from room import Room
from npc import NPC
from item import Item
from link import Link
from player import Player


class World:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.load_world()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS rooms
                               (name TEXT PRIMARY KEY, description TEXT, image BLOB)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS items
                               (name TEXT PRIMARY KEY, description TEXT, image BLOB)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS npcs
                               (name TEXT PRIMARY KEY, description TEXT, image BLOB)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS links
                               (source_room TEXT, target_room TEXT, direction TEXT,
                                FOREIGN KEY(source_room) REFERENCES rooms(name),
                                FOREIGN KEY(target_room) REFERENCES rooms(name),
                                PRIMARY KEY (source_room, target_room, direction))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS players
                               (name TEXT PRIMARY KEY, current_room TEXT, online INTEGER)''')
        self.conn.commit()
          
    def connect_database(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        
    def load_world(self):
        self.rooms = self.get_rooms()
        self.items = self.get_items()
        self.links = self.get_links()
        self.npcs = self.get_npcs()
        self.players = self.get_players()
        
    def add_player(self, player):
        self.connect_database()
        self.cursor.execute("INSERT INTO players VALUES (?, ?, ?)",
                            (player.name, player.current_room, int(player.online)))
        self.conn.commit()

    def add_room(self, room):
        self.connect_database()
        self.cursor.execute("INSERT INTO rooms VALUES (?, ?, ?)",
                            (room.name,
                             room.description, 
                             img_to_blob(room.image)))
        self.conn.commit()

    def add_item(self, item):
        self.connect_database()
        self.cursor.execute("INSERT INTO items VALUES (?, ?, ?)",
                            (item.name,
                             item.description,
                             img_to_blob(item.image)))
        self.conn.commit()

    def add_npc(self, npc):
        self.connect_database()
        self.cursor.execute("INSERT INTO npcs VALUES (?, ?, ?)",
                            (npc.name,
                             npc.description,
                             img_to_blob(npc.image)))
        self.conn.commit()

    def add_link(self, source_room, target_room, direction):
        self.connect_database()
        self.cursor.execute("INSERT INTO links VALUES (?, ?, ?)",
                            (source_room.name, target_room.name, direction))
        #create the back link
        self.cursor.execute("INSERT INTO links VALUES (?, ?, ?)",
                            (target_room.name, source_room.name, opposite_direction(direction)))
        self.conn.commit()

    def get_rooms(self):
        self.connect_database()
        self.cursor.execute("SELECT * FROM rooms")
        rows = self.cursor.fetchall()
        rooms = {}
        for row in rows:
            room = Room(*row)
            rooms[room.name] = room            
        return rooms

    def get_items(self):
        self.connect_database()
        self.cursor.execute("SELECT * FROM items")
        rows = self.cursor.fetchall()
        items = {}
        for row in rows:
            item = Item(*row)
            items[item.name] = item
        return items

    def get_npcs(self):
        self.connect_database()
        self.cursor.execute("SELECT * FROM npcs")
        rows = self.cursor.fetchall()
        npcs = {}
        for row in rows:
            npc = NPC(*row)
            npcs[npc.name] = npc
        return npcs

    def get_links(self):
        self.connect_database()
        self.cursor.execute("SELECT * FROM links")
        rows = self.cursor.fetchall()
        links = {}
        for row in rows:
            link = Link(*row)
            links[(link.source_room, link.action)] = link.target_room            
        return links  
    
    def get_players(self):
        self.connect_database()
        self.cursor.execute("SELECT * FROM players")
        rows = self.cursor.fetchall()
        players = {}
        for row in rows:
            name, current_room, online = row
            player = Player(name, current_room, bool(online))
            players[player.name] = player
        return players

    def update_player(self, player):
        self.connect_database()
        self.cursor.execute("UPDATE players SET current_room = ?, online = ? WHERE name = ?",
                            (player.current_room, int(player.online), player.name))
        self.conn.commit()
    
        
def opposite_direction(direction):
    if direction == "north":
        return "south"
    elif direction == "south":
        return "north"
    elif direction == "east":
        return "west"
    elif direction == "west":
        return "east"
    
def img_to_blob(image):
    image = Image.open(image)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_byte = buffered.getvalue()
    blob = sqlite3.Binary(img_byte)  
    return blob 
    
def blob_to_img(blob):
    image = Image.open(io.BytesIO(blob))
    return image
    
