"""
File: ui_builder_project/compiler/templates.py
Description: Stores the foundational HTML boilerplate for the compiler.
"""

def get_html_skeleton(page_title: str, inner_html: str) -> str:
    """
    Wraps the generated UI elements inside a responsive, mobile-framed HTML document.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <style>
        /* Global CSS Reset & Layout */
        body {{ 
            background-color: #f1f5f9; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0; 
            font-family: 'Segoe UI', sans-serif; 
        }}
        
        /* The Simulated Device Screen */
        .mobile-frame {{ 
            position: relative; 
            width: 375px; 
            height: 667px; 
            background-color: #ffffff; 
            overflow-y: auto; 
            overflow-x: hidden; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.1); 
            border-radius: 30px; 
            border: 12px solid #1e293b; 
        }}
        
        /* Ensures absolute coordinates map exactly to the top-left of the screen */
        .ui-element {{ 
            position: absolute; 
            box-sizing: border-box; 
        }}
    </style>
</head>
<body>
    <div class="mobile-frame">
{inner_html}
    </div>
</body>
</html>
"""
