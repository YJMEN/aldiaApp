import os
import sqlite3

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'aldiaapp.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn