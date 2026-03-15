import os
import re
from datetime import datetime

# Read SSC Mains Batch_.html as template
TEMPLATE_FILE = 'SSC Mains Batch_.html'
TXT_DIR = 'TXT'
OUT_DIR = 'HTML'

VIDEO_PAT = re.compile(r'(.*?)(?:\||-|:)\s*(https?://\S+)')
PDF_PAT = re.compile(r'(.*?)(?:\||-|:)\s*(https?://\S+\.pdf)')

def extract_links(text):
    videos = []
    pdfs = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m_pdf = PDF_PAT.match(line)
        if m_pdf:
            pdfs.append({'title': m_pdf.group(1).strip(), 'url': m_pdf.group(2).strip()})
            continue
        m_vid = VIDEO_PAT.match(line)
        if m_vid:
            url = m_vid.group(2).strip()
            if not url.lower().endswith('.pdf'):
                videos.append({'title': m_vid.group(1).strip(), 'url': url})
    return videos, pdfs

def html_escape(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))

def make_html(batch_name, videos, pdfs, date_str, template):
    # Insert video and pdf sections into template
    html = template
    # Replace title
    html = re.sub(r'<title>.*?</title>', f'<title>{html_escape(batch_name)}</title>', html)
    # Replace h1
    html = re.sub(r'<h1>.*?</h1>', f'<h1>{html_escape(batch_name)}</h1>', html)
    # Replace date
    html = re.sub(r'<div class="conversion-info">.*?<div><i class="fas fa-clock"></i>.*?</div>',
                  f'<div class="conversion-info">\g<0>\n  <div><i class="fas fa-clock"></i> {html_escape(date_str)}</div>',
                  html, flags=re.DOTALL)
    # Replace video/pdf lists (simple, assumes one section each)
    html = re.sub(r'(<h2>Videos</h2>\s*<ul>).*?(</ul>)',
        r'\1' + ''.join([f'<li><span class="video-title">{html_escape(v["title"])}:</span> <a href="{v["url"]}" target="_blank">🎬 Video</a></li>' for v in videos]) + r'\2',
        html, flags=re.DOTALL)
    html = re.sub(r'(<h2>PDFs</h2>\s*<ul>).*?(</ul>)',
        r'\1' + ''.join([f'<li><span class="pdf-title">{html_escape(p["title"])}:</span> <a href="{p["url"]}" target="_blank">📄 PDF</a></li>' for p in pdfs]) + r'\2',
        html, flags=re.DOTALL)
    return html

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(TEMPLATE_FILE, encoding='utf-8') as f:
        template = f.read()
    for fname in os.listdir(TXT_DIR):
        if not fname.endswith('.txt'):
            continue
        with open(os.path.join(TXT_DIR, fname), encoding='utf-8') as f:
            text = f.read()
        batch_name = os.path.splitext(fname)[0]
        date_str = datetime.now().strftime('%Y-%m-%d at %H:%M:%S')
        videos, pdfs = extract_links(text)
        html = make_html(batch_name, videos, pdfs, date_str, template)
        outname = os.path.join(OUT_DIR, batch_name + '.html')
        with open(outname, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Converted {fname} -> {outname}")

if __name__ == '__main__':
    main()
