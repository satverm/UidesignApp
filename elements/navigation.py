"""
File: ui_builder_project/elements/navigation.py
Description: Contains structural navigation components like Menu Bars and Icons.
Handles parsing comma-separated strings into individual clickable menu items.
"""

from .base_element import UIElement

class IconElement(UIElement):
    """
    A clickable icon (like a Hamburger menu, back arrow, or home icon).
    """
    def render_html(self, target_page_url: str = "") -> str:
        css = self.get_base_css() + " display: flex; justify-content: center; align-items: center; font-size: 24px; cursor: pointer; color: #333; text-decoration: none;"
        icon_symbol = self.extra_attr.get("icon", "☰")
        
        onclick_attr = f" onclick=\"window.location.href='{target_page_url}'\"" if target_page_url else ""
        
        return f'<div class="ui-element burger-icon" style="{css}"{onclick_attr}>{icon_symbol}</div>\n'


class MenuBarElement(UIElement):
    """
    A horizontal navigation bar. 
    Parses a string like "Home, About, Contact" into spaced HTML spans.
    """
    def render_html(self, target_page_url: str = "") -> str:
        css = self.get_base_css() + " background-color: #1e293b; color: white; display: flex; align-items: center; padding: 0 15px; font-size: 14px; font-family: sans-serif;"
        
        icon_symbol = self.extra_attr.get("icon", "☰")
        items_str = self.extra_attr.get("items", "")
        
        # Split the string by commas and wrap each item in a span
        items_list = [i.strip() for i in items_str.split(',') if i.strip()]
        item_html = "".join([f'<span style="margin-left: 15px; cursor: pointer;">{item}</span>' for item in items_list])
        
        return f'<div class="ui-element menubar" style="{css}"><span>{icon_symbol}</span>{item_html}</div>\n'
