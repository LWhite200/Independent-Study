"""
coder_agent.py
Agent that creates basic HTML and CSS files.
"""

import os

class CoderAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def build_site(self, plan, output_dir):
        """Build HTML and CSS files based on the plan dictionary."""
        print(f"\n[{self.name}] Building site...")

        # Basic shared CSS
        css = """
body {
    font-family: Arial, sans-serif;
    background-color: %s;
    margin: 40px;
}
nav a {
    margin-right: 10px;
    text-decoration: none;
    color: blue;
}
        """ % ("#f2f2f2" if not plan["use_custom_style"] else "#d0f0c0")

        # Write CSS file
        with open(os.path.join(output_dir, "style.css"), "w", encoding="utf-8") as f:
            f.write(css)

        # Helper: build HTML with optional nav
        def build_html(title, body):
            nav_html = ""
            if plan["include_nav"]:
                nav_html = "<nav><a href='index.html'>Home</a>"
                if plan["include_about"]:
                    nav_html += "<a href='about.html'>About</a>"
                if plan["include_contact"]:
                    nav_html += "<a href='contact.html'>Contact</a>"
                if plan["include_login"]:
                    nav_html += "<a href='login.html'>Login</a>"
                nav_html += "</nav><hr>"

            return f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
{nav_html}
{body}
</body>
</html>"""

        # Main index page
        with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(build_html("Home", "<h1>Welcome to the Simple Site</h1>"))

        # Optional pages
        if plan["include_about"]:
            with open(os.path.join(output_dir, "about.html"), "w", encoding="utf-8") as f:
                f.write(build_html("About", "<h2>About Us</h2><p>This is a basic about page.</p>"))

        if plan["include_contact"]:
            with open(os.path.join(output_dir, "contact.html"), "w", encoding="utf-8") as f:
                f.write(build_html("Contact", "<h2>Contact Us</h2><p>Email: example@example.com</p>"))

        if plan["include_login"]:
            login_html = """
<h2>Login</h2>
<form>
    <label>Username:</label><input type="text"><br>
    <label>Password:</label><input type="password"><br>
    <button type="submit">Login</button>
</form>
"""
            with open(os.path.join(output_dir, "login.html"), "w", encoding="utf-8") as f:
                f.write(build_html("Login", login_html))

        print(f"[{self.name}] ✅ Website files created.")
