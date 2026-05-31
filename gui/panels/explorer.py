"""
File: ui_builder_project/gui/panels/explorer.py
Description: The Project Explorer panel.
Renders the hierarchical Treeview of Pages and Elements. Handles user 
selections and the creation of new UI components in the database.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json

class ExplorerPanel:
    def __init__(self, parent_frame, db_manager, on_selection_change):
        """
        Args:
            parent_frame (ttk.Frame): The Tkinter frame to pack this panel into.
            db_manager (DatabaseManager): The active database connection.
            on_selection_change (callable): Callback function triggered when 
                                            a node is selected. Passes (node_type, id).
        """
        self.frame = parent_frame
        self.db = db_manager
        self.on_selection_change = on_selection_change
        self.active_page_id = None
        
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        # Action Buttons
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x", pady=(0, 5))
        ttk.Button(btn_frame, text="+ Page", command=self.add_page).pack(side="left", expand=True, fill="x", padx=(0, 2))
        ttk.Button(btn_frame, text="+ Element", command=self.add_element).pack(side="left", expand=True, fill="x", padx=(2, 0))

        # Treeview
        self.tree = ttk.Treeview(self.frame, show="tree")
        self.tree.pack(expand=True, fill="both")
        self.tree.bind('<<TreeviewSelect>>', self.handle_select)

    def add_page(self):
        """Creates a new blank page in the database."""
        self.db.execute_query("INSERT INTO pages (name, parent_id) VALUES (?, ?)", ("New Page", None))
        self.refresh()

    def add_element(self):
        """Creates a new default button element on the currently active page."""
        if not self.active_page_id:
            messagebox.showwarning("Warning", "Please select a Page to add an element to.")
            return
            
        default_attr = json.dumps({"text": "New Button"})
        self.db.execute_query('''
            INSERT INTO elements (page_id, name, type, x, y, width, height, extra_attr) 
            VALUES (?, 'New Element', 'button', 50, 50, 150, 40, ?)
        ''', (self.active_page_id, default_attr))
        self.refresh()

    def refresh(self):
        """Wipes and redraws the Treeview based on current database state."""
        self.tree.delete(*self.tree.get_children())
        
        # 1. Map Pages
        pages = self.db.fetch_all("SELECT id, name, parent_id FROM pages")
        page_nodes = {}
        
        # Add root pages
        for p_id, name, parent_id in pages:
            if parent_id is None:
                node = self.tree.insert("", "end", f"page_{p_id}", text=f"📄 {name}")
                page_nodes[p_id] = f"page_{p_id}"
                
        # Add subpages
        for p_id, name, parent_id in pages:
            if parent_id is not None and parent_id in page_nodes:
                self.tree.insert(page_nodes[parent_id], "end", f"page_{p_id}", text=f"↳ 📄 {name}")
                page_nodes[p_id] = f"page_{p_id}"
                
        # 2. Map Elements
        elements = self.db.fetch_all("SELECT id, page_id, name, type FROM elements")
        for e_id, p_id, name, e_type in elements:
            if p_id in page_nodes:
                self.tree.insert(page_nodes[p_id], "end", f"elem_{e_id}", text=f"↳ [{e_type}] {name}")
                
        # Expand all nodes
        for item in self.tree.get_children():
            self.tree.item(item, open=True)

    def handle_select(self, event):
        """Fires the callback to inform the main window of a selection change."""
        selected = self.tree.selection()
        if not selected: 
            return
            
        node_id = selected[0]
        node_type, db_id = node_id.split("_")
        
        if node_type == "page":
            self.active_page_id = int(db_id)
        elif node_type == "elem":
            # Find the parent page of this element to keep it active
            page_id = self.db.fetch_one("SELECT page_id FROM elements WHERE id=?", (int(db_id),))[0]
            self.active_page_id = page_id
            
        self.on_selection_change(node_type, int(db_id))
