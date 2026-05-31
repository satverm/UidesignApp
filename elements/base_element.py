"""
File: ui_builder_project/elements/base_element.py
Description: The foundational Abstract Base Class for all UI elements.
Defines the standard attributes (x, y, width, height) and enforces 
rendering methods that all sub-classes must implement.
"""

from abc import ABC, abstractmethod
import json

class UIElement(ABC):
    """
    Abstract base class representing a generic visual element on a page.
    """
    
    def __init__(self, element_id: int, page_id: int, name: str, elem_type: str, 
                 x: int, y: int, width: int, height: int, extra_attr: dict):
        """
        Initializes the base properties shared by all UI elements.
        
        Args:
            element_id (int): Unique database ID.
            page_id (int): The ID of the page this element belongs to.
            name (str): Internal identifier name.
            elem_type (str): The element category (e.g., 'button', 'input').
            x (int): Horizontal pixel coordinate.
            y (int): Vertical pixel coordinate.
            width (int): Pixel width.
            height (int): Pixel height.
            extra_attr (dict): JSON-parsed dictionary of context-specific attributes.
        """
        self.id = element_id
        self.page_id = page_id
        self.name = name
        self.type = elem_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.extra_attr = extra_attr
        
        # Target Page ID is populated later if the element has a routing flow
        self.target_page_id = None 

    @abstractmethod
    def render_html(self, target_page_url: str = "") -> str:
        """
        Compiles the element into an absolute-positioned HTML string.
        Must be overridden by all subclasses.
        
        Args:
            target_page_url (str): The filename to link to if this element 
                                   triggers a navigation flow (e.g., 'dashboard.html').
                                   
        Returns:
            str: A valid HTML element string.
        """
        pass

    def get_base_css(self) -> str:
        """
        Generates the standard absolute positioning CSS string used by all elements.
        
        Returns:
            str: Inline CSS defining position and dimensions.
        """
        return f"position: absolute; left: {self.x}px; top: {self.y}px; width: {self.width}px; height: {self.height}px; box-sizing: border-box;"

    @classmethod
    def from_db_row(cls, row: tuple):
        """
        Factory method to instantiate an element from a SQLite database row.
        Assumes row order: (id, page_id, name, type, x, y, width, height, extra_attr)
        """
        element_id, page_id, name, elem_type, x, y, w, h, extra_raw = row
        extra_attr = json.loads(extra_raw) if extra_raw else {}
        
        return cls(element_id, page_id, name, elem_type, x, y, w, h, extra_attr)

