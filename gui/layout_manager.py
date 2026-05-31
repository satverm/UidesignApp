"""
File: ui_builder_project/gui/layout_manager.py
Description: Manages the dynamic docking and layout of the Tkinter panels.
Allows switching between a 3-column desktop view and a split mobile view.
"""

import tkinter as tk

class LayoutManager:
    def __init__(self, root):
        self.root = root
        self.current_layout = None
        
    def clear_workspace(self):
        """Destroys existing paned windows to reset the grid."""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.PanedWindow):
                widget.destroy()

    def apply_desktop_layout(self, frame_tree, frame_attr, frame_preview):
        """
        Applies a 3-column vertical layout: [ Tree | Attributes | Preview ]
        """
        if self.current_layout == "desktop": 
            return
            
        self.clear_workspace()
        self.current_layout = "desktop"
        
        main_paned = tk.PanedWindow(self.root, orient="horizontal", sashrelief="raised", sashwidth=6)
        main_paned.pack(expand=True, fill="both", padx=5, pady=5)
        
        main_paned.add(frame_tree, minsize=200)
        main_paned.add(frame_attr, minsize=250)
        main_paned.add(frame_preview, minsize=400)

    def apply_mobile_layout(self, frame_tree, frame_attr, frame_preview):
        """
        Applies a stacked layout: 
        [ Tree | Attributes ]
        [     Preview       ]
        """
        if self.current_layout == "mobile": 
            return
            
        self.clear_workspace()
        self.current_layout = "mobile"
        
        # Main Vertical Split
        main_paned = tk.PanedWindow(self.root, orient="vertical", sashrelief="raised", sashwidth=6)
        main_paned.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Top Horizontal Split (Tree and Attributes share the top half)
        top_paned = tk.PanedWindow(main_paned, orient="horizontal", sashrelief="raised", sashwidth=6)
        top_paned.add(frame_tree, minsize=200)
        top_paned.add(frame_attr, minsize=250)
        
        # Add to Main
        main_paned.add(top_paned, minsize=250)
        main_paned.add(frame_preview, minsize=400)
