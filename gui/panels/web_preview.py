"""
File: ui_builder_project/gui/panels/web_preview.py
Description: The embedded live web preview panel.
Uses tkinterweb to render the compiled HTML directly inside the Tkinter GUI.
Refreshes automatically when the user applies changes.
"""

import tkinter as tk
from tkinter import ttk
import os
import config

try:
    from tkinterweb import HtmlFrame
    HAS_TKINTERWEB = True
except ImportError:
    HAS_TKINTERWEB = False

class WebPreviewPanel:
    def __init__(self, parent_frame):
        """
        Args:
            parent_frame (ttk.Frame): The Tkinter frame to pack this panel into.
        """
        self.frame = parent_frame
        self.html_frame = None
        self.setup_ui()

    def setup_ui(self):
        # Top bar for refresh controls
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Label(control_frame, text="Live Render:", font=("Arial", 10, "bold")).pack(side="left")
        ttk.Button(control_frame, text="🔄 Manual Refresh", command=self.reload_preview).pack(side="right")

        # The Web Frame
        if HAS_TKINTERWEB:
            # HtmlFrame embeds a web browser engine directly into Tkinter
            self.html_frame = HtmlFrame(self.frame, messages_enabled=False)
            self.html_frame.pack(expand=True, fill="both")
        else:
            # Fallback if the user hasn't installed tkinterweb
            fallback = tk.Canvas(self.frame, bg="#1e293b")
            fallback.pack(expand=True, fill="both")
            fallback.create_text(
                200, 200, 
                text="Please run:\npip install tkinterweb\n\nto enable the embedded live preview.", 
                fill="#10b981", font=("Consolas", 12), justify="center"
            )

    def load_page(self, page_name: str):
        if not HAS_TKINTERWEB:
            return
            
        filename = f"{page_name.replace(' ', '_')}.html"
        
        # Point directly to our background Dev Server!
        server_url = f"http://localhost:{config.DEFAULT_PORT}/{filename}"
        self.html_frame.load_url(server_url)


    def reload_preview(self):
        """Forces the embedded browser to refresh its current page."""
        if HAS_TKINTERWEB and self.html_frame:
            # Simple workaround to force reload: re-load the current URL
            current_url = self.html_frame.current_url
            if current_url:
                self.html_frame.load_url(current_url)

