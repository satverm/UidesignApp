"""
File: ui_builder_project/core/database.py
Description: Core database management layer.
Handles the SQLite connection, enforces the relational schema, and provides
helper methods for CRUD operations. 

Schema Structure:
- pages: Hierarchical UI screens.
- elements: Visual components (buttons, inputs) linked to a specific page.
- flows: Linear navigation logic linking an element to a target page.

Note: Uses PRAGMA foreign_keys = ON. Deleting a parent row will CASCADE 
and automatically delete all associated child rows to prevent orphaned data.
"""

import sqlite3
import json

class DatabaseManager:
    """
    Manages the active SQLite database connection and state for the UI Builder.
    """
    
    def __init__(self, db_path=":memory:"):
        """
        Initializes the database connection.
        
        Args:
            db_path (str): Path to the SQLite file. Defaults to ":memory:" 
                           for new, unsaved projects.
        """
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.setup_schema()

    def connect(self):
        """
        Establishes the connection to SQLite and explicitly turns on 
        foreign key constraints for relational integrity.
        """
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")

    def setup_schema(self):
        """
        Creates the foundational tables (pages, elements, flows) if they 
        do not currently exist in the connected database.
        """
        cursor = self.conn.cursor()
        
        # 1. Pages Table (The screen hierarchy)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_id INTEGER,
                FOREIGN KEY(parent_id) REFERENCES pages(id) ON DELETE CASCADE
            )
        ''')
        
        # 2. Elements Table (The UI components)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS elements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                x INTEGER DEFAULT 0,
                y INTEGER DEFAULT 0,
                width INTEGER DEFAULT 100,
                height INTEGER DEFAULT 40,
                extra_attr TEXT DEFAULT '{}',
                FOREIGN KEY(page_id) REFERENCES pages(id) ON DELETE CASCADE
            )
        ''')
        
        # 3. Flows Table (The linear navigation routing)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                element_id INTEGER NOT NULL UNIQUE,
                target_page_id INTEGER NOT NULL,
                FOREIGN KEY(element_id) REFERENCES elements(id) ON DELETE CASCADE,
                FOREIGN KEY(target_page_id) REFERENCES pages(id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def execute_query(self, query, params=()):
        """
        Executes a single INSERT, UPDATE, or DELETE SQL statement.
        
        Args:
            query (str): The SQL query string.
            params (tuple): Variables to inject into the SQL query safely.
            
        Returns:
            int: The Row ID of the last modified row.
        """
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.lastrowid

    def fetch_all(self, query, params=()):
        """
        Executes a SELECT statement and fetches all matching rows.
        
        Args:
            query (str): The SQL SELECT query string.
            params (tuple): Variables to inject into the SQL query safely.
            
        Returns:
            list: A list of tuples containing the row data.
        """
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
        
    def fetch_one(self, query, params=()):
        """
        Executes a SELECT statement and fetches a single row.
        
        Args:
            query (str): The SQL SELECT query string.
            params (tuple): Variables to inject into the SQL query safely.
            
        Returns:
            tuple: A single tuple containing the row data, or None.
        """
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    def close(self):
        """Safely commits any pending transactions and closes the connection."""
        if self.conn:
            self.conn.commit()
            self.conn.close()

