#!/usr/bin/env python3

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1]).resolve()
STATIC = ROOT / "static"

if not (ROOT / "main.py").is_file():
    raise SystemExit("ERROR: Original main.py was not found.")

if not STATIC.is_dir():
    raise SystemExit("ERROR: Original static directory was not found.")

# فقط فایل‌های موجود رابط کاربری ویرایش می‌شوند.
HTML_FILES = sorted(STATIC.glob("*.html"))

if not HTML_FILES:
    raise SystemExit("ERROR: No original HTML pages were found.")

CSS = r"""
/* POMP NET MOHAMMAD — brand layer */
:root {
  --pomp-purple: #8B35FF;
  --pomp-blue: #168CFF;
  --pomp-pink: #FF3DBB;
  --pomp-bg: #050509;
  --pomp-glass: rgba(18, 16, 31, .78);
  --pomp-border: rgba(139, 53, 255, .28);
}

html {
  color-scheme: dark;
  background: var(--pomp-bg);
}

body {
  background-color: var(--pomp-bg) !important;
  font-family: Vazirmatn, Tahoma, sans-serif !important;
}

button, input, select, textarea {
  font-family: inherit;
}

a, button {
  -webkit-tap-highlight-color: transparent;
}

button, [role="button"] {
  transition:
    border-color .2s ease,
    box-shadow .2s ease,
    transform .2s ease;
}

button:hover, [role="button"]:hover {
  border-color: var(--pomp-purple);
  box-shadow: 0 0 18px rgba(139, 53, 255, .17);
}

input, select, textarea {
  border-color: var(--pomp-border);
}

:where(.card, .panel, .glass, [class*="card"], [class*="panel"]) {
  border-color: var(--pomp-border);
}

:where(.text-teal-400, .text-cyan-400, .text-emerald-400) {
  color: #B78BFF !important;
}

:where(.bg-teal-500, .bg-cyan-500, .bg-emerald-500) {
  background-color: var(--pomp-purple) !important;
}

:where(.border-teal-500, .border-cyan-500, .border-emerald-500) {
  border-color: var(--pomp-purple) !important;
}

::selection {
  color: #fff;
  background: rgba(139, 53, 255, .65);
}

@media (max-width: 640px) {
  body {
    overflow-x: hidden;
  }

  button, input, select {
    max-width: 100%;
  }
}
"""

# لوگوی SVG اختصاصی
LOGO = """<svg xmlns="http://www.w3.org/2000/svg"
viewBox="0 0 240 240" role="img" aria-label="POMP NET MOHAMMAD">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#8B35FF"/>
    <stop offset="55%" stop-color="#168CFF"/>
    <stop offset="100%" stop-color="#FF3DBB"/>
  </linearGradient>
  <filter id="glow">
    <feGaussianBlur stdDeviation="5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect x="8" y="8" width="224" height="224" rx="58"
fill="#080710" stroke="url(#g)" stroke-width="5"/>
<path d="M58 172V68h42c27 0 42 14 42 37s-15 37-42 37H83"
fill="none" stroke="url(#g)" stroke-width="17"
stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>
<path d="M145 172V68h18l29 41 29-41h5v104"
fill="none" stroke="#fff" stroke-opacity=".9"
stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

def replace_brand(text):
    replacements = [
        (r"(?i)SPiDER\s*PANEL", "POMP NET MOHAMMAD"),
        (r"(?i)Spider\s*Panel", "POMP NET MOHAMMAD"),
        (r"(?i)SpiderPanel", "POMP NET MOHAMMAD"),
        (r"(?i)Spider\s*Panel\s*v\d+", "POMP NET MOHAMMAD"),
        (r"(?i)spider-logo\.svg", "/static/pompnet-logo.svg"),
    ]

    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)

    # تنظیم زبان و جهت صفحه برای رابط فارسی
    text = re.sub(
        r"<html\b([^>]*)>",
        lambda m: (
            "<html"
            + re.sub(r'\s(?:lang|dir)=["\'][^"\']*["\']', "", m.group(1),
                     flags=re.I)
            + ' lang="fa" dir="rtl">'
        ),
        text,
        count=1,
        flags=re.I,
    )

    # عنوان اختصاصی پنل
    if re.search(r"<title\b[^>]*>.*?</title>", text, flags=re.I | re.S):
        text = re.sub(
            r"<title\b[^>]*>.*?</title>",
            "<title>POMP NET MOHAMMAD | پنل مدیریت</title>",
            text,
            count=1,
            flags=re.I | re.S,
        )

    # CSS به انتهای head اضافه می‌شود تا استایل اصلی تا حد امکان حفظ شود.
    if "POMP NET MOHAMMAD — brand layer" not in text:
        if re.search(r"</head\s*>", text, flags=re.I):
            text = re.sub(
                r"</head\s*>",
                "<style>" + CSS + "</style>\n</head>",
                text,
                count=1,
                flags=re.I,
            )
        else:
            text = "<style>" + CSS + "</style>\n" + text

    return text

STATIC.mkdir(parents=True, exist_ok=True)

for html_file in HTML_FILES:
    original = html_file.read_text(encoding="utf-8")
    updated = replace_brand(original)

    if updated != original:
        html_file.write_text(updated, encoding="utf-8")
        print("Branded:", html_file.relative_to(ROOT))
    else:
        print("No changes needed:", html_file.relative_to(ROOT))

(STATIC / "pompnet-logo.svg").write_text(LOGO, encoding="utf-8")

# تأیید وجود فایل‌های حیاتی؛ چیزی حذف نمی‌شود.
required = [
    ROOT / "main.py",
    ROOT / "requirements.txt",
    STATIC / "index.html",
]

missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]

if missing:
    raise SystemExit("ERROR: Required files missing: " + ", ".join(missing))

print("POMP NET branding step completed.")
print("Original backend files were not rewritten by this script.")
