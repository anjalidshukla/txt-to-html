import os
import re
from datetime import datetime
import sys

# 10+ ultra-modern themes with emojis

# TOODLE THEME with 10+ ultra-stylish, colorful, modern, aesthetic HTML themes
THEMES = [
    {"name": "Toodle Neon Aurora 🌈", "vars": {"--bg-color": "#1a1a40", "--text-color": "#f8f8ff", "--primary-color": "#ff00cc", "--secondary-color": "#00fff0", "--card-bg": "#23235b", "--font-family": "'Orbitron', 'Inter', sans-serif"}},
    {"name": "Toodle Pastel Dream ☁️", "vars": {"--bg-color": "#f8fafc", "--text-color": "#6d6875", "--primary-color": "#b5838d", "--secondary-color": "#ffb4a2", "--card-bg": "#fcd5ce", "--font-family": "'Quicksand', 'Inter', sans-serif"}},
    {"name": "Toodle Cyberpunk Pulse 💾", "vars": {"--bg-color": "#0f1021", "--text-color": "#f72585", "--primary-color": "#7209b7", "--secondary-color": "#3a0ca3", "--card-bg": "#4361ee33", "--font-family": "'Share Tech Mono', 'Inter', monospace"}},
    {"name": "Toodle Emerald Forest 🌲", "vars": {"--bg-color": "#014421", "--text-color": "#e9ffdb", "--primary-color": "#38b000", "--secondary-color": "#9ef01a", "--card-bg": "#38b00022", "--font-family": "'Montserrat', 'Inter', sans-serif"}},
    {"name": "Toodle Royal Gold 👑", "vars": {"--bg-color": "#fffbe0", "--text-color": "#3d2c00", "--primary-color": "#ffd700", "--secondary-color": "#ffb300", "--card-bg": "#fffbe0", "--font-family": "'Cinzel', 'Inter', serif"}},
    {"name": "Toodle Bubblegum Pop 🍬", "vars": {"--bg-color": "#ffe0f7", "--text-color": "#ff5eae", "--primary-color": "#ff5eae", "--secondary-color": "#a685e2", "--card-bg": "#ffe0f7", "--font-family": "'Baloo 2', 'Inter', cursive"}},
    {"name": "Toodle Oceanic Wave 🌊", "vars": {"--bg-color": "#0a9396", "--text-color": "#e9d8a6", "--primary-color": "#005f73", "--secondary-color": "#94d2bd", "--card-bg": "#94d2bd33", "--font-family": "'Maven Pro', 'Inter', sans-serif"}},
    {"name": "Toodle Lime Fizz 🥤", "vars": {"--bg-color": "#e9ff70", "--text-color": "#232526", "--primary-color": "#b4ec51", "--secondary-color": "#429321", "--card-bg": "#e9ff70", "--font-family": "'Fredoka', 'Inter', sans-serif"}},
    {"name": "Toodle Rose Quartz 🌹", "vars": {"--bg-color": "#e55d87", "--text-color": "#fff", "--primary-color": "#5fc3e4", "--secondary-color": "#e55d87", "--card-bg": "#5fc3e433", "--font-family": "'Dancing Script', 'Inter', cursive"}},
    {"name": "Toodle Midnight Blue 🦋", "vars": {"--bg-color": "#232946", "--text-color": "#eebbc3", "--primary-color": "#b8c1ec", "--secondary-color": "#232946", "--card-bg": "#393053", "--font-family": "'Poppins', 'Inter', sans-serif"}},
    {"name": "Toodle Sakura Spring 🌸", "vars": {"--bg-color": "#fff0f6", "--text-color": "#d72660", "--primary-color": "#f46036", "--secondary-color": "#2e294e", "--card-bg": "#fff0f6", "--font-family": "'Satisfy', 'Inter', cursive"}},
    {"name": "Toodle Arctic Ice ❄️", "vars": {"--bg-color": "#e0fbfc", "--text-color": "#293241", "--primary-color": "#3d5a80", "--secondary-color": "#98c1d9", "--card-bg": "#e0fbfc", "--font-family": "'Titillium Web', 'Inter', sans-serif"}},
]

NAME = "\U000134B0ＳＨＩＶ\U000134EA"  # 𓆰ＳＨＩＶ𓆪

# Regex patterns for extracting info
topic_pattern = re.compile(r"^(.*?)\s*[-:]\s*(.*?)(https?://\S+)", re.MULTILINE)
pdf_pattern = re.compile(r"(PDF|Syllabus|Attachment|Notes|Handout)[^:]*: (https?://\S+)", re.IGNORECASE)
video_pattern = re.compile(r"(Class|Lecture|Video)[^:]*: (https?://\S+)", re.IGNORECASE)


def extract_links(text):
    topics = []
    pdfs = []
    videos = []
    for line in text.splitlines():
        # Try to extract topic + link
        m = topic_pattern.match(line)
        if m:
            topics.append({"title": m.group(1).strip(), "desc": m.group(2).strip(), "url": m.group(3).strip()})
            continue
        # PDF
        m = pdf_pattern.search(line)
        if m:
            pdfs.append({"title": m.group(1).strip(), "url": m.group(2).strip()})
            continue
        # Video
        m = video_pattern.search(line)
        if m:
            videos.append({"title": m.group(1).strip(), "url": m.group(2).strip()})
            continue
    return topics, pdfs, videos


def html_escape(text):
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;"))


def make_html(batch_name, topics, pdfs, videos, total_links, date_str):

    # Top 10 online CSS themes (Bootswatch + Material)
    online_themes = [
        {"name": "Bootstrap Default", "cdn": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"},
        {"name": "Cerulean", "cdn": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.2/dist/cerulean/bootstrap.min.css"},
        {"name": "Darkly", "cdn": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.2/dist/darkly/bootstrap.min.css"},
        {"name": "Flatly", "cdn": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.2/dist/flatly/bootstrap.min.css"},
        {"name": "Lux", "cdn": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.2/dist/lux/bootstrap.min.css"},
        {"name": "Materia", "cdn": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.2/dist/materia/bootstrap.min.css"},
        {"name": "Pulse", "cdn": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.2/dist/pulse/bootstrap.min.css"},
        {"name": "Sandstone", "cdn": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.2/dist/sandstone/bootstrap.min.css"},
        {"name": "Solar", "cdn": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.2/dist/solar/bootstrap.min.css"},
        {"name": "Superhero", "cdn": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.2/dist/superhero/bootstrap.min.css"},
    ]


    # Theme dropdown button
    theme_dropdown = '''<div class="theme-dropdown">
      <button class="theme-main-btn" onclick="toggleThemeDropdown()">🎨 Theme</button>
      <div id="theme-dropdown-list" class="theme-dropdown-list">
        ''' + "".join([
            f'<button class="theme-option-btn" onclick="setOnlineTheme({i})">{t["name"]}</button>' for i, t in enumerate(online_themes)
        ]) + '''
      </div>
    </div>'''

    # Topic Name button with file links
    import glob
    topic_files = sorted(glob.glob('txt/*.txt'))
    topic_buttons = '<div class="topic-files-section"><button class="topic-name-main" disabled>TOPIC NAME</button>'
    for f in topic_files:
        fname = os.path.basename(f)
        htmlfile = 'HTML/' + fname.replace('.txt', '.html')
        topic_buttons += f'<a class="topic-file-link" href="../{htmlfile}" target="_blank">{fname.replace('.txt','')}</a>'
    topic_buttons += '</div>'

    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{html_escape(batch_name)}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
      .theme-dropdown {{ position: relative; display: inline-block; }}
      .theme-main-btn {{ background: #fff; color: #232526; font-weight: 900; border: 2px solid #ff00cc; border-radius: 8px; padding: 10px 22px; font-size: 1.1rem; letter-spacing: 2px; cursor: pointer; }}
      .theme-dropdown-list {{ display: none; position: absolute; left: 0; top: 110%; background: #fff; border: 1px solid #ccc; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.15); z-index: 100; min-width: 220px; padding: 8px 0; }}
      .theme-dropdown-list .theme-option-btn {{ display: block; width: 100%; background: none; border: none; text-align: left; padding: 10px 18px; font-size: 1rem; color: #232526; cursor: pointer; border-radius: 0; transition: background 0.2s; }}
      .theme-dropdown-list .theme-option-btn:hover {{ background: #f0f0f0; }}
      .controls {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-bottom: 25px; }}
    </style>
    <link id="online-theme-link" rel="stylesheet" href="" disabled>
</head>
<body>
<h1>{html_escape(batch_name)}</h1>
<div class="conversion-info">
    <div><i class="fas fa-magic"></i> Converted by: {NAME}</div>
    <div><i class="fas fa-clock"></i> {html_escape(date_str)}</div>
</div>
<div class="meta-info">
    <div class="total-links">
        <i class="fas fa-link"></i> Total links: {total_links}
    </div>
</div>
<div class="controls">{theme_dropdown}</div>
{topic_buttons}
<div id="topics-section">
{grouped_topics_html(topics)}
</div>
<script>
const onlineThemes = {str([t['cdn'] for t in online_themes])};
function toggleThemeDropdown() {{
  const list = document.getElementById('theme-dropdown-list');
  list.style.display = (list.style.display === 'block') ? 'none' : 'block';
}}
function setOnlineTheme(idx) {{
  const link = document.getElementById('online-theme-link');
  link.removeAttribute('disabled');
  link.href = onlineThemes[idx];
  document.body.className = '';
  document.body.style.fontFamily = '';
  document.getElementById('theme-dropdown-list').style.display = 'none';
}}
document.addEventListener('click', function(e) {{
  const dropdown = document.querySelector('.theme-dropdown');
  if (dropdown && !dropdown.contains(e.target)) {{
    document.getElementById('theme-dropdown-list').style.display = 'none';
  }}
}});
</script>
</body>
</html>'''
    return html

# Group topics by detected headings
def grouped_topics_html(topics):
    from collections import defaultdict
    import re
    topic_groups = defaultdict(list)
    for t in topics:
        # Extract topic heading (before first dash, pipe, or parenthesis)
        m = re.match(r"([A-Za-z0-9 .&]+)", t['title'])
        heading = m.group(1).strip() if m else t['title']
        topic_groups[heading].append(t)
    html = ''
    for heading, items in topic_groups.items():
        html += f'<h2>{html_escape(heading)}</h2><ul>'
        for t in items:
            html += f'<li>{html_escape(t["title"]) + ": " + html_escape(t["desc"])} <a href="{t["url"]}" target="_blank">🔗 Link</a></li>'
        html += '</ul>'
    return html
    return html


def convert_folder(folder, out_folder):
    os.makedirs(out_folder, exist_ok=True)
    for fname in os.listdir(folder):
        if fname.endswith('.txt'):
            with open(os.path.join(folder, fname), encoding='utf-8') as f:
                text = f.read()
            topics, pdfs, videos = extract_links(text)
            total_links = len(topics) + len(pdfs) + len(videos)
            batch_name = os.path.splitext(fname)[0]
            date_str = datetime.now().strftime('%Y-%m-%d at %H:%M:%S')
            html = make_html(batch_name, topics, pdfs, videos, total_links, date_str)
            outname = os.path.join(out_folder, batch_name + '.html')
            with open(outname, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Converted {fname} -> {outname}")

def get_folder_paths():
    import argparse
    parser = argparse.ArgumentParser(description="TXT to HTML batch converter")
    parser.add_argument('-i', '--input', help='Input folder containing .txt files')
    parser.add_argument('-o', '--output', help='Output folder for .html files')
    args = parser.parse_args()
    input_folder = args.input
    output_folder = args.output
    if not input_folder:
        input_folder = input('Enter input folder path (default: txt): ').strip() or 'txt'
    if not output_folder:
        output_folder = input('Enter output folder path (default: HTML): ').strip() or 'HTML'
    return input_folder, output_folder

if __name__ == "__main__":
    input_folder, output_folder = get_folder_paths()
    convert_folder(input_folder, output_folder)
