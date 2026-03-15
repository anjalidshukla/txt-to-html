import os
import re
from datetime import datetime
import sys

# 10+ ultra-modern themes with emojis
THEMES = [
    {"name": "Neon Night 🌃", "vars": {"--bg-color": "#18122B", "--text-color": "#F6F1F1", "--primary-color": "#635DFF", "--secondary-color": "#FF6B6B", "--card-bg": "#393053"}},
    {"name": "Sunset Vibe 🌅", "vars": {"--bg-color": "#FFDEE9", "--text-color": "#232526", "--primary-color": "#FF6A00", "--secondary-color": "#FFD200", "--card-bg": "#FFF1EB"}},
    {"name": "Aqua Dream 🐬", "vars": {"--bg-color": "#43C6AC", "--text-color": "#191654", "--primary-color": "#191654", "--secondary-color": "#43C6AC", "--card-bg": "#A2F1FC"}},
    {"name": "Cyberpunk 💾", "vars": {"--bg-color": "#0F2027", "--text-color": "#FF00CC", "--primary-color": "#00DBDE", "--secondary-color": "#FC00FF", "--card-bg": "#232526"}},
    {"name": "Pastel Pop 🍭", "vars": {"--bg-color": "#F8FFAE", "--text-color": "#43C6AC", "--primary-color": "#A770EF", "--secondary-color": "#FDB99B", "--card-bg": "#FDEB71"}},
    {"name": "Emerald Forest 🌲", "vars": {"--bg-color": "#348F50", "--text-color": "#F9F9F9", "--primary-color": "#56B870", "--secondary-color": "#348F50", "--card-bg": "#56B870"}},
    {"name": "Royal Gold 👑", "vars": {"--bg-color": "#FDC830", "--text-color": "#373B44", "--primary-color": "#373B44", "--secondary-color": "#F37335", "--card-bg": "#FFF6B7"}},
    {"name": "Bubblegum Bliss 🍬", "vars": {"--bg-color": "#FBD3E9", "--text-color": "#333", "--primary-color": "#BB377D", "--secondary-color": "#FBD3E9", "--card-bg": "#BB377D22"}},
    {"name": "Oceanic Wave 🌊", "vars": {"--bg-color": "#2193b0", "--text-color": "#fff", "--primary-color": "#6dd5ed", "--secondary-color": "#2193b0", "--card-bg": "#6dd5ed33"}},
    {"name": "Lime Fizz 🥤", "vars": {"--bg-color": "#B4EC51", "--text-color": "#232526", "--primary-color": "#429321", "--secondary-color": "#B4EC51", "--card-bg": "#EDE574"}},
    {"name": "Rose Quartz 🌹", "vars": {"--bg-color": "#E55D87", "--text-color": "#fff", "--primary-color": "#5FC3E4", "--secondary-color": "#E55D87", "--card-bg": "#5FC3E433"}},
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
    # Theme toggle buttons
    theme_buttons = "".join([
        f'<button class="theme-toggle" onclick="setTheme({i})">{t["name"]}</button>' for i, t in enumerate(THEMES)
    ])
    html = f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{html_escape(batch_name)}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
  <style>
    :root {{ --bg-color: #18122B; --text-color: #F6F1F1; --primary-color: #635DFF; --secondary-color: #FF6B6B; --card-bg: #393053; }}
    {theme_vars}
    body {{ background: var(--bg-color); color: var(--text-color); font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif; min-height: 100vh; margin: 0; padding: 16px; transition: all 0.3s; }}
    h1 {{ text-align: center; font-size: 2.2rem; font-weight: 800; margin: 12px 0 6px 0; }}
    .conversion-info {{ text-align: center; margin: 4px 0 12px 0; font-size: 0.95rem; opacity: 0.8; }}
    .meta-info {{ background: var(--card-bg); border-radius: 10px; padding: 14px; margin: 8px auto 20px auto; max-width: 380px; text-align: center; font-size: 1rem; font-weight: 600; }}
    .total-links {{ font-weight: 700; font-size: 1.1rem; }}
    .controls {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-bottom: 25px; }}
    .theme-toggle {{ padding: 10px 20px; background: var(--primary-color); border: none; border-radius: 8px; cursor: pointer; color: var(--text-color); font-size: 0.95rem; font-weight: 600; margin: 2px; }}
    ul {{ list-style-type: none; padding: 0; margin: 0; }}
    li {{ background: var(--card-bg); margin: 10px 0; padding: 14px 16px; border-radius: 10px; font-size: 1rem; display: flex; flex-direction: column; gap: 4px; }}
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
function setTheme(idx) {{
  document.body.className = 'theme-' + idx;
  currentTheme = idx;
}}
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
