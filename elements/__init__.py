"""
File: ui_builder_project/elements/__init__.py
Description: Exposes the element classes and provides a Factory function
to instantiate the correct class type from a raw database row.
"""

from .buttons import ButtonElement
from .inputs import InputElement, TextboxElement
from .typography import HeadingElement, SubheadingElement, LabelElement
from .navigation import IconElement, MenuBarElement
from.inputs import DatePickerElement

def create_element(db_row: tuple):
    """
    Factory function to generate the correct UIElement subclass based on the database type.
    
    Args:
        db_row (tuple): A raw SQLite row from the 'elements' table.
                        Format: (id, page_id, name, type, x, y, width, height, extra_attr)
                        
    Returns:
        UIElement: An instantiated subclass of UIElement.
    """
    elem_type = db_row[3] # Index 3 is the 'type' column
    
    # Map the database string to the appropriate Python Class
    class_map = {
        "button": ButtonElement,
        "input": InputElement,
        "textbox": TextboxElement,
        "date": DatePickerElement, # Date uses the Input layout with different HTML type
        "heading": HeadingElement,
        "subheading": SubheadingElement,
        "label": LabelElement,
        "icon": IconElement,
        "menubar": MenuBarElement
    }
    
    # Fallback to LabelElement if the type is unknown to prevent crashing
    element_class = class_map.get(elem_type, LabelElement)
    
    # Instantiate and return the object
    return element_class.from_db_row(db_row)
