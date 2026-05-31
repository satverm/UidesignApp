"""
File: ui_builder_project/core/project_manager.py
Description: Project lifecycle management.
Handles the heavy lifting for creating new projects, saving/loading .uidb files, 
and injecting standard UI templates into the active database.
"""

import sqlite3
import os
import json
from .database import DatabaseManager

class ProjectManager:
    """
    Manages project file operations and template generation.
    """
    
    @staticmethod
    def create_new_project(db_manager: DatabaseManager):
        """
        Wipes the current database and sets up a fresh schema.
        
        Args:
            db_manager (DatabaseManager): The active database connection instance.
        """
        if db_manager.conn:
            db_manager.conn.close()
        
        # Connect to a fresh in-memory database
        db_manager.db_path = ":memory:"
        db_manager.connect()
        db_manager.setup_schema()

    @staticmethod
    def save_project(db_manager: DatabaseManager, target_filepath: str):
        """
        Backs up the active (usually in-memory) database to a physical .uidb file.
        
        Args:
            db_manager (DatabaseManager): The active database connection instance.
            target_filepath (str): The absolute path where the file should be saved.
        """
        file_conn = sqlite3.connect(target_filepath)
        with file_conn:
            db_manager.conn.backup(file_conn)
        file_conn.close()

    @staticmethod
    def load_project(db_manager: DatabaseManager, source_filepath: str):
        """
        Loads a physical .uidb file into the active database session.
        
        Args:
            db_manager (DatabaseManager): The active database connection instance.
            source_filepath (str): The absolute path of the file to load.
            
        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        if not os.path.exists(source_filepath):
            raise FileNotFoundError(f"Project file not found: {source_filepath}")
            
        file_conn = sqlite3.connect(source_filepath)
        
        # Reset current connection to fresh memory, then backup file into it
        if db_manager.conn:
            db_manager.conn.close()
            
        db_manager.db_path = ":memory:"
        db_manager.connect()
        
        with db_manager.conn:
            file_conn.backup(db_manager.conn)
        file_conn.close()

    @staticmethod
    def load_business_template(db_manager: DatabaseManager):
        """
        Wipes the current project and injects a standard 5-page business 
        template complete with linked elements and linear flows.
        """
        ProjectManager.create_new_project(db_manager)
        
        # 1. Insert Standard Pages
        pages = [
            (1, 'Home', None), 
            (2, 'About Us', None), 
            (3, 'Services', None), 
            (4, 'Contact', None), 
            (5, 'User Dashboard', 1)
        ]
        db_manager.conn.executemany("INSERT INTO pages (id, name, parent_id) VALUES (?, ?, ?)", pages)
        
        # 2. Insert Standard Elements
        elements = [
            # Home Page
            (1, 1, 'Header', 'heading', 20, 40, 300, 40, json.dumps({"text": "Welcome to Our App"})),
            (2, 1, 'LoginBtn', 'button', 20, 100, 150, 40, json.dumps({"text": "Login to Dashboard"})),
            # Contact Page
            (3, 4, 'NameInput', 'input', 20, 100, 250, 40, json.dumps({"hint": "John Doe", "label": "Full Name"})),
            (4, 4, 'SubmitBtn', 'button', 20, 170, 250, 40, json.dumps({"text": "Send Message"})),
            # Dashboard Page
            (5, 5, 'DashTitle', 'heading', 20, 40, 200, 40, json.dumps({"text": "User Dashboard"})),
            (6, 5, 'LogoutBtn', 'button', 20, 100, 150, 40, json.dumps({"text": "Logout"}))
        ]
        db_manager.conn.executemany('''
            INSERT INTO elements (id, page_id, name, type, x, y, width, height, extra_attr) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', elements)
        
        # 3. Insert Routing Flows
        flows = [
            (2, 5),  # Home LoginBtn -> User Dashboard
            (6, 1)   # Dashboard LogoutBtn -> Home
        ]
        db_manager.conn.executemany("INSERT INTO flows (element_id, target_page_id) VALUES (?, ?)", flows)
        
        db_manager.conn.commit()
