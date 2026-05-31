"""
File: ui_builder_project/elements/inputs.py
Description: Contains data-entry element classes (Textboxes, Inputs).
Handles composite HTML rendering where a single UI element might require 
wrapping divs and linked labels.
"""

from .base_element import UIElement

class InputElement(UIElement):
    """
    Standard single-line text input field, optionally paired with a label.
    """
    
    def render_html(self, target_page_url: str = "") -> str:
        # The base CSS is applied to a wrapper div, not the input directly
        css = self.get_base_css() + " display: flex; flex-direction: column;"
        
        hint = self.extra_attr.get("hint", "")
        label_text = self.extra_attr.get("label", "")
        
        html = f'        <div class="input-group ui-element" style="{css}">\n'
        
        # Render the label above the input if it was provided
        if label_text:
            html += f'            <label style="font-weight: bold; font-size: 14px; margin-bottom: 5px; color: #333; font-family: sans-serif;">{label_text}</label>\n'
            
        # The input stretches to fill the remainder of the bounding box
        html += f'            <input type="text" placeholder="{hint}" style="width: 100%; height: 100%; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px; box-sizing: border-box; font-family: sans-serif;">\n'
        
        html += '        </div>\n'
        return html

class DatePickerElement(UIElement):
    def render_html(self, target_page_url: str = "") -> str:
        css = self.get_base_css() + " display: flex; flex-direction: column;"
        label_text = self.extra_attr.get("label", "")
        
        html = f'        <div class="input-group ui-element" style="{css}">\n'
        if label_text:
            html += f'            <label style="font-weight: bold; font-size: 14px; margin-bottom: 5px; color: #333; font-family: sans-serif;">{label_text}</label>\n'
        
        # Specific type="date" ensures browsers render a calendar
        html += f'            <input type="date" style="width: 100%; height: 100%; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px; box-sizing: border-box; font-family: sans-serif;">\n'
        html += '        </div>\n'
        return html


class TextboxElement(UIElement):
    """
    Multi-line text area for larger text inputs (e.g., messages, bios).
    """
    
    def render_html(self, target_page_url: str = "") -> str:
        css = self.get_base_css() + " display: flex; flex-direction: column;"
        
        hint = self.extra_attr.get("hint", "")
        label_text = self.extra_attr.get("label", "")
        
        html = f'        <div class="input-group ui-element" style="{css}">\n'
        if label_text:
            html += f'            <label style="font-weight: bold; font-size: 14px; margin-bottom: 5px; color: #333; font-family: sans-serif;">{label_text}</label>\n'
            
        html += f'            <textarea placeholder="{hint}" style="width: 100%; height: 100%; resize: none; border: 1px solid #cbd5e1; border-radius: 4px; padding: 8px; box-sizing: border-box; font-family: sans-serif;"></textarea>\n'
        html += '        </div>\n'
        return html
