import os
import sqlite3
import hashlib

DB_FILE = "playstore.db"

class DB:
    def __init__(self, dbfile=DB_FILE):
        self.dbfile = dbfile
        self._init_db()

    def _init_db(self):
        if not os.path.exists(self.dbfile):
            c = self.conn().cursor()
            c.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
            c.execute("CREATE TABLE phones(id INTEGER PRIMARY KEY, name TEXT, storage_total INTEGER, storage_used INTEGER, version INTEGER)")
            c.execute("CREATE TABLE installs(id INTEGER PRIMARY KEY, phone_id INTEGER, app_id INTEGER)")
            c.execute("CREATE TABLE apps(id INTEGER PRIMARY KEY, name TEXT, size INTEGER, min_version INTEGER, price REAL, is_paid INTEGER)")
            c.execute("INSERT INTO phones VALUES(NULL,'Modelo A',64000,0,10)")
            c.execute("INSERT INTO phones VALUES(NULL,'Modelo B',128000,0,12)")
            c.execute("INSERT INTO phones VALUES(NULL,'Modelo C',32000,0,8)")
            apps = [
                ("ChatApp",20000,9,0.0,0),
                ("PuzzleFun",15000,8,1.99,1),
                ("Racing3D",50000,11,2.99,1),
                ("MiniTool",5000,7,0.0,0),
                ("UpcomingBattle",80000,12,0.0,0),
            ]
            for a in apps:
                c.execute("INSERT INTO apps(name,size,min_version,price,is_paid) VALUES(?,?,?,?,?)", a)
            c.connection.commit()

    def conn(self):
        return sqlite3.connect(self.dbfile)

    def create_user(self, username, password):
        h = hashlib.sha256(password.encode()).hexdigest()
        try:
            c = self.conn()
            cur = c.cursor()
            cur.execute("INSERT INTO users(username,password) VALUES(?,?)", (username, h))
            c.commit()
            c.close()
            return True, "OK"
        except Exception as e:
            return False, str(e)

    def check_user(self, username, password):
        h = hashlib.sha256(password.encode()).hexdigest()
        c = self.conn()
        cur = c.cursor()
        cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, h))
        r = cur.fetchone()
        c.close()
        return r is not None

    def get_phones(self):
        c = self.conn()
        cur = c.cursor()
        cur.execute("SELECT id,name,storage_total,storage_used,version FROM phones")
        r = cur.fetchall()
        c.close()
        return r

    def get_apps(self):
        c = self.conn()
        cur = c.cursor()
        cur.execute("SELECT id,name,size,min_version,price,is_paid FROM apps")
        r = cur.fetchall()
        c.close()
        return r

    def get_phone(self, pid):
        c = self.conn()
        cur = c.cursor()
        cur.execute("SELECT id,name,storage_total,storage_used,version FROM phones WHERE id=?", (pid,))
        r = cur.fetchone()
        c.close()
        return r

    def update_phone_used(self, pid, new_used):
        c = self.conn()
        cur = c.cursor()
        cur.execute("UPDATE phones SET storage_used=? WHERE id=?", (new_used, pid))
        c.commit(); c.close()

    def add_install(self, phone_id, app_id):
        c = self.conn()
        cur = c.cursor()
        cur.execute("INSERT INTO installs(phone_id,app_id) VALUES(?,?)", (phone_id, app_id))
        c.commit(); c.close()

    def is_installed(self, phone_id, app_id):
        c = self.conn()
        cur = c.cursor()
        cur.execute("SELECT id FROM installs WHERE phone_id=? AND app_id=?", (phone_id, app_id))
        r = cur.fetchone()
        c.close()
        return r is not None

    def get_installed(self, phone_id):
        c = self.conn()
        cur = c.cursor()
        cur.execute(
            "SELECT a.id,a.name,a.size FROM apps a JOIN installs i ON a.id=i.app_id WHERE i.phone_id=?",
            (phone_id,),
        )
        r = cur.fetchall()
        c.close()
        return r
