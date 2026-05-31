"""
File: ui_builder_project/config.py
Description: Global configuration module for the Modular UI Builder.
Defines system-wide constants, default paths, and application metadata.
This file serves as the environment context and should be imported by 
any module requiring absolute paths or global state variables.
"""

import os
from pathlib import Path

# Base Directory calculations
# Resolves to the absolute path of the 'ui_builder_project' root folder
BASE_DIR = Path(__file__).resolve().parent

# Default output locations for the HTML compiler
DEFAULT_EXPORT_DIR = BASE_DIR / "generated_website"

# Application Metadata
APP_NAME = "Modular UI Builder"
APP_VERSION = "1.0.0"

# Local Development Server Constants
DEFAULT_PORT = 8000

# File Extension for SQLite Project Saves
PROJECT_EXTENSION = ".uidb"
