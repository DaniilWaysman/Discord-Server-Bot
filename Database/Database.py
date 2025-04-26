import sqlite3
import os


class Database:
    def __init__(self, db_path="Database/database.db"):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        with self._connect() as db:
            cursor = db.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS recruit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                nickname TEXT NOT NULL,
                age INTEGER NOT NULL,
                info TEXT NOT NULL,
                status TEXT DEFAULT 'Waiting'
            )
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS giveaway (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                winners INTEGER NOT NULL,
                status TEXT DEFAULT 'Waiting'
            )
            """)

            db.commit()
            
    def add_recruit(self, message_id: int, user_id: int, nickname: str, name: str, age: int, info: str, status: str = "Waiting") -> bool:
        with self._connect() as db:
            cursor = db.cursor()
            
            cursor.execute("""
                INSERT INTO recruit (message_id, user_id, nickname, name, age, info, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (message_id, user_id, nickname, name, age, info, status))
            
            db.commit()
            return True
    
    def check_recruit_exists(self, user_id: int, status: str = "Waiting") -> bool:
        with self._connect() as db:
            cursor = db.cursor()
            
            cursor.execute("SELECT 1 FROM recruit WHERE user_id = ? AND status = ?", (user_id, status))

            result = cursor.fetchone()
            return result is not None


    def add_giveaway(self, message_id: int, channel_id: int, user_id: int, winners: int, status: str = "Waiting"):
        with self._connect() as db:
            cursor = db.cursor()
            
            cursor.execute("""
                           INSERT INTO giveaway (message_id, channel_id, user_id, winners, status)
                           VALUES (?, ?, ?, ?, ?)
                           """, (message_id, channel_id, user_id, winners, status))
            db.commit()