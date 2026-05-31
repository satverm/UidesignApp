"""
File: ui_builder_project/server/dev_server.py
Description: Background local development server.
Serves the compiled HTML files on localhost so the user can test their 
generated website with actual routing and browser rendering.
"""

import threading
import http.server
import socketserver
import os
import config

# Custom server class to prevent "Address already in use" errors when restarting
class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class DevServer:
    def __init__(self, port=config.DEFAULT_PORT, directory=config.DEFAULT_EXPORT_DIR):
        self.port = port
        self.directory = directory
        self.server = None
        self.thread = None
        self.is_running = False

    def start(self):
        """Starts the HTTP server on a daemon thread."""
        if self.is_running: 
            return
            
        # Ensure the export directory exists before serving it
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=self.directory, **kwargs)

        self.server = ReusableTCPServer(("", self.port), Handler)
        
        # Daemon thread ensures the server dies when the main Tkinter app is closed
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.is_running = True
        print(f"Dev Server running at http://localhost:{self.port}")

    def stop(self):
        """Safely shuts down the HTTP server."""
        if self.is_running and self.server:
            self.server.shutdown()
            self.server.server_close()
            self.is_running = False
            print("Dev Server stopped.")
