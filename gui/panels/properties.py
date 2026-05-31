"""
File: ui_builder_project/gui/panels/properties.py
Description: The dynamic Attributes panel.
Reads the selected element's properties from the database and generates 
the appropriate form fields. Handles saving changes back to the database.
"""

import tkinter as tk
from tkinter import ttk
import json

class PropertiesPanel:
    def __init__(self, parent_frame, db_manager, on_apply_changes):
        """
        Args:
            parent_frame (ttk.Frame): The Tkinter frame to pack this panel into.
            db_manager (DatabaseManager): The active database connection.
            on_apply_changes (callable): Callback function triggered when the user 
                                         clicks 'Apply Changes'. Triggers HTML recompile.
        """
        self.frame = parent_frame
        self.db = db_manager
        self.on_apply_changes = on_apply_changes
        self.clear()

    def clear(self):
        """Destroys all current form widgets to prepare for a new selection."""
        for widget in self.frame.winfo_children():
            widget.destroy()

    def show_empty_state(self):
        self.clear()
        ttk.Label(self.frame, text="Select a Page or Element to edit.", foreground="gray").pack(pady=20)

    def load_page_properties(self, page_id):
        """Generates the form for editing a Page."""
        self.clear()
        
        row = self.db.fetch_one("SELECT name, parent_id FROM pages WHERE id=?", (page_id,))
        if not row: return
        page_name, parent_id = row

        ttk.Label(self.frame, text="Page Properties", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0,15))
        
        ttk.Label(self.frame, text="Page Name:").pack(anchor="w")
        name_var = tk.StringVar(value=page_name)
        ttk.Entry(self.frame, textvariable=name_var).pack(fill="x", pady=(0,10))

        def save():
            self.db.execute_query("UPDATE pages SET name=? WHERE id=?", (name_var.get(), page_id))
            self.on_apply_changes()

        ttk.Button(self.frame, text="Apply Changes", command=save).pack(fill="x", pady=20)

    def load_element_properties(self, element_id):
        """Generates the highly dynamic form for editing a UI Element."""
        self.clear()
        
        row = self.db.fetch_one("SELECT name, type, x, y, width, height, extra_attr FROM elements WHERE id=?", (element_id,))
        if not row: return
        name, e_type, x, y, w, h, extra_raw = row
        extra = json.loads(extra_raw) if extra_raw else {}

        ttk.Label(self.frame, text=f"Element: {e_type.capitalize()}", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0,15))
        
        # 1. Base Attributes
        ttk.Label(self.frame, text="Internal Name:").pack(anchor="w")
        name_var = tk.StringVar(value=name)
        ttk.Entry(self.frame, textvariable=name_var).pack(fill="x", pady=(0,10))

        # 2. Layout (X, Y, Width, Height)
        layout_frame = ttk.LabelFrame(self.frame, text="Layout (X, Y, W, H)", padding=5)
        layout_frame.pack(fill="x", pady=5)
        
        x_var = tk.StringVar(value=str(x))
        y_var = tk.StringVar(value=str(y))
        w_var = tk.StringVar(value=str(w))
        h_var = tk.StringVar(value=str(h))
        
        ttk.Entry(layout_frame, textvariable=x_var, width=6).grid(row=0, column=0, padx=2)
        ttk.Entry(layout_frame, textvariable=y_var, width=6).grid(row=0, column=1, padx=2)
        ttk.Entry(layout_frame, textvariable=w_var, width=6).grid(row=0, column=2, padx=2)
        ttk.Entry(layout_frame, textvariable=h_var, width=6).grid(row=0, column=3, padx=2)

        # 3. Contextual Attributes based on type
        context_frame = ttk.Frame(self.frame)
        context_frame.pack(fill="x", pady=10)
        
        text_var = tk.StringVar(value=extra.get("text", ""))
        hint_var = tk.StringVar(value=extra.get("hint", ""))
        items_var = tk.StringVar(value=extra.get("items", ""))
        
        if e_type in ["button", "heading", "subheading", "label"]:
            ttk.Label(context_frame, text="Display Text:").pack(anchor="w")
            ttk.Entry(context_frame, textvariable=text_var).pack(fill="x")
        elif e_type in ["input", "textbox"]:
            ttk.Label(context_frame, text="Placeholder/Hint Text:").pack(anchor="w")
            ttk.Entry(context_frame, textvariable=hint_var).pack(fill="x")
        elif e_type == "menubar":
            ttk.Label(context_frame, text="Menu Items (Comma Separated):").pack(anchor="w")
            ttk.Entry(context_frame, textvariable=items_var).pack(fill="x")

        # 4. Routing Flow (Only for buttons or icons)
        target_page_var = tk.StringVar()
        if e_type in ["button", "icon"]:
            ttk.Label(self.frame, text="On Click Go To:").pack(anchor="w", pady=(10, 0))
            
            # Get pages for dropdown
            pages = self.db.fetch_all("SELECT id, name FROM pages")
            options = ["None"] + [f"{p_name} (ID: {p_id})" for p_id, p_name in pages]
            
            # Check current flow
            flow = self.db.fetch_one("SELECT target_page_id FROM flows WHERE element_id=?", (element_id,))
            if flow:
                t_name = next((n for pid, n in pages if pid == flow[0]), "Unknown")
                target_page_var.set(f"{t_name} (ID: {flow[0]})")
            else:
                target_page_var.set("None")
                
            ttk.Combobox(self.frame, textvariable=target_page_var, values=options).pack(fill="x")

        def save():
            # Package extra attributes into JSON
            new_extra = {"text": text_var.get(), "hint": hint_var.get(), "items": items_var.get()}
            
            self.db.execute_query('''
                UPDATE elements SET name=?, x=?, y=?, width=?, height=?, extra_attr=? WHERE id=?
            ''', (name_var.get(), int(x_var.get()), int(y_var.get()), int(w_var.get()), int(h_var.get()), json.dumps(new_extra), element_id))
            
            # Save linear flow
            if e_type in ["button", "icon"]:
                t_val = target_page_var.get()
                if t_val == "None" or not t_val:
                    self.db.execute_query("DELETE FROM flows WHERE element_id=?", (element_id,))
                else:
                    t_id = int(t_val.split("(ID: ")[1].replace(")", ""))
                    self.db.execute_query("REPLACE INTO flows (element_id, target_page_id) VALUES (?, ?)", (element_id, t_id))
            
            self.on_apply_changes()

        ttk.Button(self.frame, text="Apply Changes", command=save).pack(fill="x", pady=20)
