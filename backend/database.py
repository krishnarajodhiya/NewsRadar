"""
Database module for handling SQLite operations
"""
import sqlite3
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "predictions.db"


def init_db():
    """Initialize the SQLite database"""
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def save_prediction(text, prediction, confidence):
    """
    Save a prediction to the database
    
    Args:
        text (str): The article/headline text
        prediction (str): 'REAL' or 'FAKE'
        confidence (float): Confidence score (0-1)
    
    Returns:
        int: The ID of the inserted record
    """
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO predictions (text, prediction, confidence)
        VALUES (?, ?, ?)
    ''', (text, prediction, confidence))
    
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    
    return record_id


def get_recent_predictions(limit=10):
    """
    Get recent predictions from database
    
    Args:
        limit (int): Number of recent predictions to retrieve
    
    Returns:
        list: List of predictions as dictionaries
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM predictions
        ORDER BY created_at DESC
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_total_predictions():
    """Get total number of predictions made"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM predictions')
    count = cursor.fetchone()[0]
    conn.close()
    
    return count


def get_stats():
    """Get statistics about predictions"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT prediction, COUNT(*) as count
        FROM predictions
        GROUP BY prediction
    ''')
    
    stats = {}
    for row in cursor.fetchall():
        stats[row[0]] = row[1]
    
    conn.close()
    
    return stats


def clear_predictions():
    """Clear all predictions from database"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM predictions')
    conn.commit()
    conn.close()
