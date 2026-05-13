import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH

class Database:
    """Database class for managing user data."""
    
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id, first_name, username):
        """Add or update a user in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (id, first_name, username, last_seen)
            VALUES (?, ?, ?, ?)
        ''', (user_id, first_name, username, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id):
        """Get a user by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        return user
    
    def get_all_users(self):
        """Get all users from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        conn.close()
        
        return [{'id': u[0], 'first_name': u[1], 'username': u[2], 'created_at': u[3]} for u in users]
    
    def get_total_users(self):
        """Get the total number of users."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def get_active_users(self):
        """Get the number of active users (last seen in last 7 days)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM users
            WHERE last_seen > datetime('now', '-7 days')
        ''')
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def get_user_stats(self, user_id):
        """Get statistics for a specific user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM messages WHERE user_id = ?
        ''', (user_id,))
        message_count = cursor.fetchone()[0]
        conn.close()
        
        return {'messages_sent': message_count}
    
    def add_message(self, user_id, message_text):
        """Add a message to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (user_id, message_text)
            VALUES (?, ?)
        ''', (user_id, message_text))
        
        conn.commit()
        conn.close()
