import sqlite3
import os


class Database:
    def __init__(self, db_path="Database/database.db"):
        self.db_path = db_path
        self._create_table()
        
        
    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as db:
            cursor = db.cursor()
            
            query = """
            CREATE TABLE IF NOT EXISTS mutes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    duration INTEGER,
                    adm INTEGER NOT NULL
                    )   
            """
            
            cursor.execute(query)
            db.commit()

    
    def give_mute(self, user_id: int, reason: str, duration: int, adm: int):
        with self._connect() as db:
            cursor = db.cursor()
            cursor.execute(""" INSERT INTO mutes (
                user_id,
                reason,
                duration,
                adm) VALUES (?, ?, ?, ? ) """, (user_id, reason, duration, adm)
                )
            db.commit()
