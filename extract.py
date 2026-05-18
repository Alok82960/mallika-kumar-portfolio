import re

with open('C:\\Users\\HP\\Downloads\\mallika-kumar-portfolio-main\\frontend\\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract and remove CSS
style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
if style_match:
    css_content = style_match.group(1).strip()
    with open('C:\\Users\\HP\\Downloads\\mallika-kumar-portfolio-main\\frontend\\style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    html = html.replace(style_match.group(0), '<link rel="stylesheet" href="style.css">')

# Extract and remove JS
script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if script_match:
    js_content = script_match.group(1).strip()
    with open('C:\\Users\\HP\\Downloads\\mallika-kumar-portfolio-main\\frontend\\main.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    html = html.replace(script_match.group(0), '<script src="main.js"></script>')

with open('C:\\Users\\HP\\Downloads\\mallika-kumar-portfolio-main\\frontend\\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Extracted CSS and JS successfully.")
