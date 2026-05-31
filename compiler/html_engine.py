"""
File: ui_builder_project/compiler/html_engine.py
Description: The core HTML compiler.
Reads the active database, instantiates Python objects using the element factory,
compiles their HTML, and writes the output files to the target directory.
"""

import os
from core.database import DatabaseManager
from elements import create_element
from compiler.templates import get_html_skeleton
import config

class HTMLEngine:
    def __init__(self, db_manager: DatabaseManager, output_dir: str = config.DEFAULT_EXPORT_DIR):
        self.db = db_manager
        self.output_dir = output_dir

    def compile(self):
        """
        Executes the full build process, transforming the database into an HTML website.
        """
        # Ensure output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # 1. Fetch and map all pages
        pages_raw = self.db.fetch_all("SELECT id, name FROM pages")
        if not pages_raw:
            print("Compiler: No pages to compile.")
            return

        # Create a dictionary to map Page IDs to clean HTML filenames
        page_map = {p_id: name.replace(" ", "_") for p_id, name in pages_raw}

        # 2. Iterate through each page to build its file
        for p_id, p_name in page_map.items():
            filepath = os.path.join(self.output_dir, f"{p_name}.html")
            inner_html = ""

            # Fetch all elements belonging to this page
            elements_raw = self.db.fetch_all('''
                SELECT id, page_id, name, type, x, y, width, height, extra_attr 
                FROM elements WHERE page_id=?
            ''', (p_id,))

            # 3. Object-Oriented Rendering
            for raw_row in elements_raw:
                # Instantiate the correct class (Button, Input, MenuBar, etc.)
                element_obj = create_element(raw_row)
                
                # Check if this element triggers a navigation flow
                flow_raw = self.db.fetch_one("SELECT target_page_id FROM flows WHERE element_id=?", (element_obj.id,))
                target_url = ""
                
                if flow_raw and flow_raw[0] in page_map:
                    # Resolve the target page ID to its physical HTML filename
                    target_url = f"{page_map[flow_raw[0]]}.html"

                # Ask the object to render itself, passing the routing URL if it exists
                inner_html += element_obj.render_html(target_page_url=target_url)

            # 4. Wrap the generated elements in the master skeleton and save
            final_html = get_html_skeleton(p_name.replace('_', ' '), inner_html)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(final_html)
                
        print(f"Compiler: Successfully built {len(page_map)} pages in '{self.output_dir}'")

