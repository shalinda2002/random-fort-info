from flask import Flask, jsonify, Response, render_template
import random
import json
import os
import base64
import requests
from io import BytesIO

app = Flask(__name__)

# Load forts from JSON file
def load_forts():
    """Load forts data from JSON file"""
    json_path = os.path.join(os.path.dirname(__file__), 'maharashtra_forts.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load forts dynamically to avoid caching issues
def get_forts():
    return load_forts()

forts = get_forts()

def fetch_image_as_base64(url):
    """Fetch an image URL and return as base64 data URI"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            if 'svg' in content_type:
                content_type = 'image/svg+xml'
            elif 'png' in content_type:
                content_type = 'image/png'
            else:
                content_type = 'image/jpeg'
            encoded = base64.b64encode(response.content).decode('utf-8')
            return f"data:{content_type};base64,{encoded}"
    except:
        pass
    return None

def wrap_text(text, max_chars=60):
    """Wrap text to fit within the card"""
    if not text:
        return ["No description available."]

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + " " + word) <= max_chars:
            current_line = current_line + " " + word if current_line else word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

        # Limit to 4 lines
        if len(lines) >= 4:
            break

    if current_line and len(lines) < 4:
        lines.append(current_line)

    return lines if lines else ["No description available."]


def generate_svg_card(fort):
    """Generate a beautiful SVG card for a fort showing: image, name, about, location"""
    name = fort.get("name", "Unknown Fort")
    about = fort.get("about", "")
    image_url = fort.get("image", "")
    location = fort.get("location", "Maharashtra, India")

    # Default location if empty
    if not location:
        location = "Maharashtra"

    # Truncate location if too long
    if len(location) > 25:
        location = location[:22] + "..."

    # Wrap the about text
    wrapped_about = wrap_text(about, 65)
    about_lines = ""
    for i, line in enumerate(wrapped_about):
        y_pos = 340 + (i * 20)
        # Escape special XML characters
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        about_lines += f'<text x="20" y="{y_pos}" fill="#e0e0e0" font-size="12" font-family="Segoe UI, Arial, sans-serif">{line}</text>\n'

    if len(wrapped_about) == 4:
        about_lines += f'<text x="475" y="{340 + 60}" fill="#888" font-size="12" font-family="Segoe UI, Arial, sans-serif" text-anchor="end">...</text>\n'

    # Escape the fort name
    escaped_name = name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    # Truncate name if too long
    display_name = escaped_name if len(escaped_name) <= 35 else escaped_name[:32] + "..."

    # Default placeholder image if none provided
    if not image_url:
        image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Flag_of_the_Maratha_Empire.svg/200px-Flag_of_the_Maratha_Empire.svg.png"

    # Fetch image and convert to base64 for GitHub compatibility
    image_data = fetch_image_as_base64(image_url)
    if not image_data:
        # Fallback placeholder
        image_data = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0NjUiIGhlaWdodD0iMjMwIj48cmVjdCBmaWxsPSIjMmEyYTRhIiB3aWR0aD0iNDY1IiBoZWlnaHQ9IjIzMCIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmaWxsPSIjNjY2IiBmb250LXNpemU9IjE2IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+SW1hZ2UgTm90IEF2YWlsYWJsZTwvdGV4dD48L3N2Zz4="

    # Get fort index for display
    try:
        fort_index = forts.index(fort) + 1
    except ValueError:
        fort_index = 1

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="495" height="450" viewBox="0 0 495 450">
  <defs>
    <linearGradient id="cardGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#16213e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0f3460;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="titleGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#f39c12;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#e74c3c;stop-opacity:1" />
    </linearGradient>
    <clipPath id="imageClip">
      <rect x="15" y="55" width="465" height="230" rx="10"/>
    </clipPath>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="495" height="450" rx="15" fill="url(#cardGradient)" filter="url(#shadow)"/>

  <!-- Border -->
  <rect width="493" height="448" x="1" y="1" rx="14" fill="none" stroke="#e94560" stroke-width="2" opacity="0.6"/>

  <!-- Fort Name -->
  <text x="20" y="35" fill="url(#titleGradient)" font-size="20" font-weight="bold" font-family="Segoe UI, Arial, sans-serif">{display_name}</text>

  <!-- Location badge -->
  <rect x="340" y="12" width="140" height="26" rx="13" fill="#e94560" opacity="0.3"/>
  <text x="410" y="30" fill="#fff" font-size="10" font-family="Segoe UI, Arial, sans-serif" text-anchor="middle">{location}</text>

  <!-- Fort Image Background -->
  <rect x="15" y="55" width="465" height="230" rx="10" fill="#2a2a4a"/>

  <!-- Fort Image embedded as base64 for GitHub compatibility -->
  <image x="15" y="55" width="465" height="230" preserveAspectRatio="xMidYMid slice" clip-path="url(#imageClip)" href="{image_data}"/>

  <!-- Gradient overlay on image -->
  <defs>
    <linearGradient id="imageOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="70%" style="stop-color:transparent;stop-opacity:0" />
      <stop offset="100%" style="stop-color:#1a1a2e;stop-opacity:0.8" />
    </linearGradient>
  </defs>
  <rect x="15" y="55" width="465" height="230" rx="10" fill="url(#imageOverlay)"/>

  <!-- Divider -->
  <line x1="20" y1="300" x2="475" y2="300" stroke="#e94560" stroke-width="2" opacity="0.5"/>

  <!-- About section -->
  <text x="20" y="318" fill="#f39c12" font-size="11" font-weight="bold" font-family="Segoe UI, Arial, sans-serif" letter-spacing="1">ABOUT</text>
  {about_lines}

  <!-- Footer -->
  <text x="20" y="435" fill="#666" font-size="10" font-family="Segoe UI, Arial, sans-serif">Historic Forts of Maharashtra | Refresh for another fort</text>
  <text x="475" y="435" fill="#666" font-size="10" font-family="Segoe UI, Arial, sans-serif" text-anchor="end">#{fort_index}/{len(forts)}</text>
</svg>'''

    return svg

@app.route("/")
def home():
    """Render the home page with preview"""
    return render_template("index.html", total_forts=len(forts))

@app.route("/api/fort")
def get_fort():
    """Return fort data as JSON"""
    fort = random.choice(forts)
    return jsonify(fort)

@app.route("/api/all-forts")
def get_all_forts():
    """Return all forts"""
    return jsonify({"forts": forts, "total": len(forts)})

@app.route("/api/forts-by-location/<location>")
def get_forts_by_location(location):
    """Return forts filtered by location"""
    filtered = [f for f in forts if f.get("location", "").lower() == location.lower()]
    return jsonify({"forts": filtered, "total": len(filtered)})

@app.route("/api/fort-card")
@app.route("/api/fort-card.svg")
def get_fort_card():
    """Return a random fort as an SVG card - use this in GitHub README"""
    fort = random.choice(forts)
    svg = generate_svg_card(fort)

    response = Response(svg, mimetype="image/svg+xml")
    # Disable caching so each refresh shows a new fort
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["ETag"] = str(random.random())
    return response

@app.route("/api/fort/<int:fort_id>")
def get_specific_fort(fort_id):
    """Return a specific fort as an SVG card"""
    if 0 <= fort_id < len(forts):
        fort = forts[fort_id]
        svg = generate_svg_card(fort)
        response = Response(svg, mimetype="image/svg+xml")
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response
    return jsonify({"error": "Fort not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=8081)
