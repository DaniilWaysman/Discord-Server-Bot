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
            CREATE TABLE IF NOT EXISTS mutes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                reason TEXT NOT NULL,
                duration INTEGER,
                adm INTEGER NOT NULL
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS recruit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                nickname TEXT NOT NULL,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
            """)

            db.commit()

    def give_mute(self, user_id: int, reason: str, duration: int, adm: int):
        with self._connect() as db:
            cursor = db.cursor()
            cursor.execute("""
            INSERT INTO mutes (user_id, reason, duration, adm)
            VALUES (?, ?, ?, ?)
            """, (user_id, reason, duration, adm))
            db.commit()
            
                    
    def add_recruit_info(self, user_id: str, nickname: str, name: str, age: int) -> bool:
        with self._connect() as db:
            cursor = db.cursor()

            cursor.execute("SELECT * FROM recruit WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()

            if result:
                return False

            cursor.execute(""" 
                INSERT INTO recruit (user_id, nickname, name, age)
                VALUES (?, ?, ?, ?)
            """, (user_id, nickname, name, age))
            db.commit()
            return True

