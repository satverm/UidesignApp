"""
File: ui_builder_project/elements/buttons.py
Description: Contains interactive button element classes.
Inherits from UIElement and defines specific HTML/CSS compilation 
logic for standard and icon buttons.
"""

from .base_element import UIElement

class ButtonElement(UIElement):
    """
    Standard clickable button element.
    """
    
    def render_html(self, target_page_url: str = "") -> str:
        """
        Compiles the button into an HTML tag, injecting click routing if applicable.
        """
        # Base positioning combined with specific button styling
        css = self.get_base_css() + (
            "background-color: #2563eb; color: white; border: none; "
            "border-radius: 4px; cursor: pointer; font-family: sans-serif; "
            "display: flex; justify-content: center; align-items: center;"
        )
        
        text = self.extra_attr.get("text", "Button")
        
        # Inject linear flow routing if a target page was provided
        onclick_attr = f" onclick=\"window.location.href='{target_page_url}'\"" if target_page_url else ""
        
        return f'<button class="ui-element" style="{css}"{onclick_attr}>{text}</button>\n'

