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
    # Theme CSS variables
    theme_vars = "".join([
        f".theme-{i} {{\n" + "\n".join([f"  {k}: {v};" for k, v in t['vars'].items()]) + "\n}}\n"
        for i, t in enumerate(THEMES)
    ])
    # TOODLE THEME section
    theme_buttons = '<div class="toodle-theme-section"><button class="theme-toggle-main" disabled>TOODLE THEME</button>'
    theme_buttons += "".join([
        f'<button class="theme-toggle" onclick="setTheme({i})">{t["name"]}</button>' for i, t in enumerate(THEMES)
    ])
    theme_buttons += '</div>'

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
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Quicksand:wght@700&family=Share+Tech+Mono&family=Montserrat:wght@700&family=Cinzel:wght@700&family=Baloo+2:wght@700&family=Maven+Pro:wght@700&family=Fredoka:wght@700&family=Dancing+Script:wght@700&family=Poppins:wght@700&family=Satisfy&family=Titillium+Web:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg-color: #1a1a40; --text-color: #f8f8ff; --primary-color: #ff00cc; --secondary-color: #00fff0; --card-bg: #23235b; --font-family: 'Orbitron', 'Inter', sans-serif; }}
        {theme_vars}
        body {{ background: var(--bg-color); color: var(--text-color); font-family: var(--font-family, 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif); min-height: 100vh; margin: 0; padding: 16px; transition: all 0.3s; }}
        h1 {{ text-align: center; font-size: 2.2rem; font-weight: 800; margin: 12px 0 6px 0; font-family: var(--font-family, 'Inter', sans-serif); }}
        .conversion-info {{ text-align: center; margin: 4px 0 12px 0; font-size: 0.95rem; opacity: 0.8; }}
        .meta-info {{ background: var(--card-bg); border-radius: 10px; padding: 14px; margin: 8px auto 20px auto; max-width: 380px; text-align: center; font-size: 1rem; font-weight: 600; }}
        .total-links {{ font-weight: 700; font-size: 1.1rem; }}
        .controls {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-bottom: 25px; }}
        .toodle-theme-section {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 10px; }}
        .theme-toggle-main {{ background: #fff; color: #232526; font-weight: 900; border: 2px solid #ff00cc; border-radius: 8px; padding: 10px 22px; font-size: 1.1rem; margin-right: 10px; letter-spacing: 2px; cursor: default; }}
        .theme-toggle {{ padding: 10px 20px; background: var(--primary-color); border: none; border-radius: 8px; cursor: pointer; color: var(--text-color); font-size: 0.95rem; font-weight: 600; margin: 2px; font-family: var(--font-family, 'Inter', sans-serif); }}
        .theme-toggle:active {{ transform: scale(0.97); }}
        .topic-files-section {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 18px; }}
        .topic-name-main {{ background: #fff; color: #232526; font-weight: 900; border: 2px solid #00fff0; border-radius: 8px; padding: 10px 22px; font-size: 1.1rem; margin-right: 10px; letter-spacing: 2px; cursor: default; }}
        .topic-file-link {{ background: var(--primary-color); color: var(--text-color); border-radius: 8px; padding: 8px 16px; text-decoration: none; font-weight: 700; font-size: 1rem; margin: 2px; font-family: var(--font-family, 'Inter', sans-serif); transition: background 0.2s; }}
        .topic-file-link:hover {{ background: var(--secondary-color); color: #fff; }}
        ul {{ list-style-type: none; padding: 0; margin: 0; }}
        li {{ background: var(--card-bg); margin: 10px 0; padding: 14px 16px; border-radius: 10px; font-size: 1rem; display: flex; flex-direction: column; gap: 4px; font-family: var(--font-family, 'Inter', sans-serif); }}
        a {{ color: var(--primary-color); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .pdf-title {{ color: #ff7043; }}
        .video-title {{ color: #ff3d71; }}
        .topic-title {{ color: var(--secondary-color); }}
    </style>
</head>
<body class="theme-0">
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
<div class="controls">{theme_buttons}</div>
{topic_buttons}
<h2>Topics & Links</h2>
<ul>
        {''.join([f'<li><span class="topic-title">{html_escape(t["title"])}:</span> {html_escape(t["desc"])} <a href="{t["url"]}" target="_blank">🔗 Link</a></li>' for t in topics])}
</ul>
<h2>PDFs</h2>
<ul>
        {''.join([f'<li><span class="pdf-title">{html_escape(p["title"])}:</span> <a href="{p["url"]}" target="_blank">📄 PDF</a></li>' for p in pdfs])}
</ul>
<h2>Videos</h2>
<ul>
        {''.join([f'<li><span class="video-title">{html_escape(v["title"])}:</span> <a href="{v["url"]}" target="_blank">🎬 Video</a></li>' for v in videos])}
</ul>
<script>
let currentTheme = 0;
function setTheme(idx) {
    document.body.className = 'theme-' + idx;
    // Set font family for each theme
    const themeVars = getComputedStyle(document.body);
    document.body.style.fontFamily = themeVars.getPropertyValue('--font-family') || 'Inter, sans-serif';
    currentTheme = idx;
}
</script>
</body>
</html>'''
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
