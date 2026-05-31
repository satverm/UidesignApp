"""
File: ui_builder_project/main.py
Description: The Application Entry Point.
Initializes the database, starts the local development server, prepares the 
HTML compiler, and launches the Tkinter main event loop.
"""

import sys
import os

# Ensure the root directory is in the system path so imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import DatabaseManager
from core.project_manager import ProjectManager
from server.dev_server import DevServer
from compiler.html_engine import HTMLEngine

from gui.window import ApplicationWindow
from gui.panels.explorer import ExplorerPanel
from gui.panels.properties import PropertiesPanel
from gui.panels.web_preview import WebPreviewPanel

def main():
    print("Initializing Modular UI Builder...")

    # 1. Initialize the Core Database (In-Memory for a fresh start)
    db = DatabaseManager()
    
    # Optional: Pre-load the Business Template so the app isn't empty on launch
    ProjectManager.load_business_template(db)

    # 2. Initialize the HTML Compiler
    compiler = HTMLEngine(db_manager=db)

    # 3. Start the Background Local Dev Server
    server = DevServer()
    server.start()

    # 4. Compile the template immediately so the server has files to serve
    compiler.compile()

    # 5. Initialize the Tkinter GUI
    app = ApplicationWindow(db_manager=db, dev_server=server, compiler_engine=compiler)

    # 6. Instantiate the Panels and inject them into the Window's Layout Manager
    # (The ApplicationWindow created empty frames; we now fill them with our panel logic)
    
    # We define a callback: When Properties change -> Recompile HTML -> Refresh Preview
    def on_properties_applied():
        app.trigger_recompile()
        preview_panel.reload_preview()
        explorer_panel.refresh()

    properties_panel = PropertiesPanel(
        parent_frame=app.frame_attr, 
        db_manager=db, 
        on_apply_changes=on_properties_applied
    )

    # We define a callback: When Explorer selection changes -> Load new properties & preview
    def on_tree_selection(node_type, db_id):
        if node_type == "page":
            properties_panel.load_page_properties(db_id)
            
            # Fetch page name to tell the preview panel what HTML file to load
            page_name = db.fetch_one("SELECT name FROM pages WHERE id=?", (db_id,))[0]
            preview_panel.load_page(page_name)
            
        elif node_type == "elem":
            properties_panel.load_element_properties(db_id)
            
            # Find the parent page of this element to preview it
            page_id = db.fetch_one("SELECT page_id FROM elements WHERE id=?", (db_id,))[0]
            page_name = db.fetch_one("SELECT name FROM pages WHERE id=?", (page_id,))[0]
            preview_panel.load_page(page_name)

    explorer_panel = ExplorerPanel(
        parent_frame=app.frame_tree, 
        db_manager=db, 
        on_selection_change=on_tree_selection
    )

    preview_panel = WebPreviewPanel(
        parent_frame=app.frame_preview
    )

    # Initial load of the Home page in the preview panel
    preview_panel.load_page("Home")

    # 7. Start the Application Event Loop
    print("Launching GUI...")
    app.mainloop()

if __name__ == "__main__":
    main()
