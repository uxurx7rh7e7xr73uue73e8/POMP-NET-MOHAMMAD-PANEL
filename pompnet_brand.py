#!/usr/bin/env python3

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1]).resolve()
STATIC = ROOT / "static"

if not (ROOT / "main.py").is_file():
    raise SystemExit("ERROR: main.py not found")

if not STATIC.is_dir():
    raise SystemExit("ERROR: static directory not found")

html_files = sorted(STATIC.glob("*.html"))

if not html_files:
    raise SystemExit("ERROR: No HTML pages found")

CSS = r"""
/* POMP NET MOHAMMAD — CRYSTAL GLASS */
:root {
  --pomp-bg: #050509;
  --pomp-purple: #8B35FF;
  --pomp-blue: #168CFF;
  --pomp-pink: #FF3DBB;
  --pomp-glass: rgba(17, 13, 29, .82);
  --pomp-border: rgba(139, 53, 255, .28);
  --pomp-glow: 0 0 24px rgba(139, 53, 255, .13);
}

html {
  background: var(--pomp-bg);
  color-scheme: dark;
  scroll-behavior: smooth;
}

body {
  background-color: var(--pomp-bg);
  font-family: Vazirmatn, Tahoma, sans-serif;
}

button, input, select, textarea {
  font-family: inherit;
}

button, a, [role="button"] {
  -webkit-tap-highlight-color: transparent;
}

:where(
  .card,
  .panel,
  .glass,
  [class*="card"],
  [class*="panel"]
) {
  border-color: var(--pomp-border);
}

:where(
  .text-teal-400,
  .text-cyan-400,
  .text-emerald-400
) {
  color: #B78BFF !important;
}

:where(
  .bg-teal-500,
  .bg-cyan-500,
  .bg-emerald-500
) {
  background-color: var(--pomp-purple) !important;
}

:where(
  .border-teal-500,
  .border-cyan-500,
  .border-emerald-500
) {
  border-color: var(--pomp-purple) !important;
}

button:hover, [role="button"]:hover {
  box-shadow: var(--pomp-glow);
}

input, select, textarea {
  border-color: var(--pomp-border);
}

::selection {
  color: white;
  background: rgba(139, 53, 255, .65);
}

@media (max-width: 640px) {
  body {
    overflow-x: hidden;
  }

  img, video, canvas {
    max-width: 100%;
  }
}
"""

LOGO = """<svg xmlns="http://www.w3.org/2000/svg"
viewBox="0 0 240 240">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#8B35FF"/>
    <stop offset="55%" stop-color="#168CFF"/>
    <stop offset="100%" stop-color="#FF3DBB"/>
  </linearGradient>
</defs>
<rect x="8" y="8" width="224" height="224" rx="58"
fill="#050509" stroke="url(#g)" stroke-width="6"/>
<path d="M65 175V65h43c27 0 42 14 42 37s-15 37-42 37H91"
fill="none" stroke="url(#g)" stroke-width="17"
stroke-linecap="round" stroke-linejoin="round"/>
<path d="M151 175V65h12l29 42 29-42h4v110"
fill="none" stroke="#fff" stroke-opacity=".9"
stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

def brand_html(text: str) -> str:
    # نام‌های قدیمی فقط در متن HTML و رابط کاربری تغییر می‌کنند.
    replacements = [
        (r"(?i)Spider\s*Panel\s*v\d+", "POMP NET MOHAMMAD"),
        (r"(?i)Spider\s*Panel", "POMP NET MOHAMMAD"),
        (r"(?i)SpiderPanel", "POMP NET MOHAMMAD"),
        (r"(?i)SPiDER\s*PANEL", "POMP NET MOHAMMAD"),
    ]

    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)

    # زبان فارسی و جهت راست‌به‌چپ
    html_match = re.search(r"<html\b([^>]*)>", text, flags=re.I)

    if html_match:
        attrs = html_match.group(1)
        attrs = re.sub(
            r'\s+(?:lang|dir)=["\'][^"\']*["\']',
            "",
            attrs,
            flags=re.I,
        )
        text = (
            text[:html_match.start()]
            + '<html' + attrs + ' lang="fa" dir="rtl">'
            + text[html_match.end():]
        )

    # عنوان اختصاصی
    title = "<title>POMP NET MOHAMMAD | پنل مدیریت</title>"

    if re.search(r"<title\b[^>]*>.*?</title>", text, flags=re.I | re.S):
        text = re.sub(
            r"<title\b[^>]*>.*?</title>",
            title,
            text,
            count=1,
            flags=re.I | re.S,
        )
    elif re.search(r"</head\s*>", text, flags=re.I):
        text = re.sub(
            r"</head\s*>",
            title + "\n</head>",
            text,
            count=1,
            flags=re.I,
        )

    # افزودن CSS بدون حذف استایل‌ها یا اسکریپت‌های قبلی
    if "POMP NET MOHAMMAD — CRYSTAL GLASS" not in text:
        style = "\n<style>\n" + CSS + "\n</style>\n"

        if re.search(r"</head\s*>", text, flags=re.I):
            text = re.sub(
                r"</head\s*>",
                style + "</head>",
                text,
                count=1,
                flags=re.I,
            )
        else:
            text = text + style

    # لوگو به‌عنوان آیکون سایت
    if not re.search(
        r'<link\b[^>]*rel=["\']icon["\']',
        text,
        flags=re.I,
    ):
        icon = (
            '<link rel="icon" type="image/svg+xml" '
            'href="/static/pompnet-logo.svg">'
        )

        if re.search(r"</head\s*>", text, flags=re.I):
            text = re.sub(
                r"</head\s*>",
                icon + "\n</head>",
                text,
                count=1,
                flags=re.I,
            )

    return text


STATIC.mkdir(parents=True, exist_ok=True)

for path in html_files:
    original = path.read_text(encoding="utf-8")
    updated = brand_html(original)

    if updated != original:
        path.write_text(updated, encoding="utf-8")
        print("Updated:", path.relative_to(ROOT))
    else:
        print("Unchanged:", path.relative_to(ROOT))

(STATIC / "pompnet-logo.svg").write_text(LOGO, encoding="utf-8")

# بررسی فایل‌های ضروری بدون جایگزینی کد اصلی
required = [
    ROOT / "main.py",
    ROOT / "requirements.txt",
    STATIC / "index.html",
]

missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]

if missing:
    raise SystemExit("ERROR: Missing required files: " + ", ".join(missing))

print("POMP NET branding completed.")
print("The original main.py was not modified.")
