import sqlite3
import json
from datetime import datetime
import os

class Database:
    def __init__(self, db_file='security_dashboard.db'):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Scan history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                features TEXT NOT NULL,
                prediction INTEGER NOT NULL,
                confidence REAL NOT NULL,
                risk_score REAL NOT NULL,
                model_version TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                scan_id INTEGER,
                report_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (scan_id) REFERENCES scans (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    
    def add_user(self, username, email, password):
        """Add new user"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, password)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return {'success': True, 'user_id': user_id}
        except sqlite3.IntegrityError as e:
            return {'success': False, 'error': 'Username or email already exists'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_user(self, username):
        """Get user by username"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'password': user[3],
                'created_at': user[4]
            }
        return None
    
    def save_scan(self, user_id, features, prediction, confidence, risk_score, model_version):
        """Save scan to history"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scans (user_id, features, prediction, confidence, risk_score, model_version)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, json.dumps(features), prediction, confidence, risk_score, model_version))
        conn.commit()
        scan_id = cursor.lastrowid
        conn.close()
        return scan_id
    
    def get_user_scans(self, user_id, limit=50):
        """Get scan history for user"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM scans WHERE user_id = ? ORDER BY created_at DESC LIMIT ?
        ''', (user_id, limit))
        scans = cursor.fetchall()
        conn.close()
        
        return [{
            'id': s[0],
            'features': json.loads(s[2]),
            'prediction': s[3],
            'confidence': s[4],
            'risk_score': s[5],
            'model_version': s[6],
            'created_at': s[7]
        } for s in scans]
    
    def get_stats(self):
        """Get global statistics"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM scans')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM scans WHERE prediction = 1')
        high_risk = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM scans WHERE prediction = 0')
        low_risk = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(confidence) FROM scans')
        avg_confidence = cursor.fetchone()[0] or 0.0
        
        conn.close()
        
        return {
            'total_predictions': total,
            'high_risk_detected': high_risk,
            'low_risk_detected': low_risk,
            'average_confidence': avg_confidence
        }

# Global instance
db = Database()
