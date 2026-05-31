"""
File: ui_builder_project/elements/typography.py
Description: Contains text-rendering element classes (Headings, Paragraphs).
Ensures semantic HTML output (h1, h3, p) based on the chosen UI element type.
"""

from .base_element import UIElement

class HeadingElement(UIElement):
    """
    Primary page title using semantic <h1> tags.
    """
    def render_html(self, target_page_url: str = "") -> str:
        css = self.get_base_css() + " margin: 0; color: #0f172a; font-size: 24px; font-weight: bold; font-family: sans-serif;"
        text = self.extra_attr.get("text", "Heading")
        return f'<h1 class="ui-element" style="{css}">{text}</h1>\n'


class SubheadingElement(UIElement):
    """
    Secondary section title using semantic <h3> tags.
    """
    def render_html(self, target_page_url: str = "") -> str:
        css = self.get_base_css() + " margin: 0; color: #475569; font-size: 18px; font-weight: bold; font-family: sans-serif;"
        text = self.extra_attr.get("text", "Subheading")
        return f'<h3 class="ui-element" style="{css}">{text}</h3>\n'


class LabelElement(UIElement):
    """
    Standard paragraph or descriptive text using <p> tags.
    """
    def render_html(self, target_page_url: str = "") -> str:
        css = self.get_base_css() + " margin: 0; color: #333333; font-size: 14px; font-family: sans-serif;"
        text = self.extra_attr.get("text", "Text Label")
        return f'<p class="ui-element" style="{css}">{text}</p>\n'

