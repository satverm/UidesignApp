"""
File: ui_builder_project/simple_main.py
Description: A lightweight test harness for the Modular UI Builder.
Omits the live preview and background server to focus purely on testing
the Database CRUD operations, the GUI panels, and the HTML Compiler.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Ensure the root directory is in the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import DatabaseManager
from core.project_manager import ProjectManager
from compiler.html_engine import HTMLEngine

# Import only the specific panels we need
from gui.panels.explorer import ExplorerPanel
from gui.panels.properties import PropertiesPanel

def main():
    print("Initializing Simple Test Harness...")

    # 1. Initialize Core Components
    db = DatabaseManager()
    ProjectManager.load_business_template(db)
    compiler = HTMLEngine(db_manager=db)

    # 2. Setup Basic Tkinter Root
    root = tk.Tk()
    root.title("Modular UI Builder - Simple Test Mode")
    root.geometry("800x600")

    # 3. Top Toolbar (For Manual Compilation)
    toolbar = ttk.Frame(root, padding=10, relief="raised")
    toolbar.pack(side="top", fill="x")
    
    def manual_compile():
        compiler.compile()
        messagebox.showinfo("Success", f"HTML files compiled successfully to:\n{compiler.output_dir}")

    ttk.Button(toolbar, text="⚙️ Compile HTML", command=manual_compile).pack(side="left")
    ttk.Label(toolbar, text="Test Mode: Live Preview Disabled", foreground="gray").pack(side="right")

    # 4. Main Layout (Two Panes)
    paned_window = tk.PanedWindow(root, orient="horizontal", sashrelief="raised", sashwidth=6)
    paned_window.pack(expand=True, fill="both", padx=10, pady=10)

    frame_tree = ttk.LabelFrame(paned_window, text="Project Explorer")
    frame_attr = ttk.LabelFrame(paned_window, text="Properties")
    
    paned_window.add(frame_tree, minsize=250)
    paned_window.add(frame_attr, minsize=300)

    # 5. Initialize the Panels and Callbacks
    def on_properties_applied():
        """Callback when user clicks 'Apply Changes' in the properties panel."""
        print("Database updated.")
        explorer_panel.refresh()

    properties_panel = PropertiesPanel(
        parent_frame=frame_attr, 
        db_manager=db, 
        on_apply_changes=on_properties_applied
    )

    def on_tree_selection(node_type, db_id):
        """Callback when user clicks a Page or Element in the treeview."""
        if node_type == "page":
            properties_panel.load_page_properties(db_id)
        elif node_type == "elem":
            properties_panel.load_element_properties(db_id)

    explorer_panel = ExplorerPanel(
        parent_frame=frame_tree, 
        db_manager=db, 
        on_selection_change=on_tree_selection
    )

    # 6. Start the App
    print("Launching Simple GUI...")
    root.mainloop()

if __name__ == "__main__":
    main()
