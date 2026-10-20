#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/app").resolve()
STATIC = ROOT / "static"

if not (ROOT / "main.py").is_file():
    raise SystemExit("ERROR: Core application file not found")

if not STATIC.is_dir():
    raise SystemExit("ERROR: Static directory not found")

HTML_FILES = sorted(STATIC.rglob("*.html"))

if not HTML_FILES:
    raise SystemExit("ERROR: No HTML files found")


# ==========================================================
# POMP NET MOHAMMAD — CRYSTAL GLASS DESIGN SYSTEM
# ==========================================================

CSS = r"""
/* POMP NET MOHAMMAD | CRYSTAL GLASS */
:root {
  --pomp-bg: #050509;
  --pomp-purple: #8B35FF;
  --pomp-blue: #168CFF;
  --pomp-pink: #FF3DBB;
  --pomp-glass: rgba(15, 11, 26, .88);
  --pomp-border: rgba(139, 53, 255, .32);
  --pomp-text: #F8F5FF;
  --pomp-muted: #B7A9CC;
  --pomp-glow: 0 0 28px rgba(139, 53, 255, .17);
}

html {
  color-scheme: dark;
  scroll-behavior: smooth;
  background: var(--pomp-bg);
}

body {
  background-color: var(--pomp-bg);
  color: var(--pomp-text);
  font-family: Vazirmatn, Tahoma, sans-serif;
  -webkit-tap-highlight-color: transparent;
}

button,
input,
select,
textarea {
  font-family: inherit;
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
  color: #C5A2FF !important;
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

input,
select,
textarea {
  border-color: var(--pomp-border);
}

::selection {
  color: #fff;
  background: rgba(139, 53, 255, .7);
}

/* Premium contact menu */
.pomp-contact-dock {
  position: fixed;
  z-index: 99990;
  right: max(14px, env(safe-area-inset-right));
  bottom: max(14px, env(safe-area-inset-bottom));
  direction: rtl;
  font-family: Vazirmatn, Tahoma, sans-serif;
}

.pomp-contact-dock details {
  position: relative;
}

.pomp-contact-dock summary {
  list-style: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  border: 1px solid rgba(255,255,255,.25);
  border-radius: 999px;
  padding: 13px 18px;
  color: white;
  font-size: 13px;
  font-weight: 900;
  background: linear-gradient(
    125deg,
    rgba(139,53,255,.98),
    rgba(22,140,255,.96),
    rgba(255,61,187,.92)
  );
  box-shadow:
    0 8px 34px rgba(139,53,255,.30),
    inset 0 1px rgba(255,255,255,.25);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}

.pomp-contact-dock summary::-webkit-details-marker {
  display: none;
}

.pomp-contact-dock summary::before {
  content: "✦";
  font-size: 18px;
}

.pomp-contact-links {
  box-sizing: border-box;
  width: min(310px, calc(100vw - 28px));
  position: absolute;
  right: 0;
  bottom: calc(100% + 12px);
  display: grid;
  gap: 9px;
  padding: 14px;
  border: 1px solid rgba(139,53,255,.42);
  border-radius: 22px;
  background: rgba(8,7,16,.96);
  box-shadow:
    0 18px 55px rgba(0,0,0,.55),
    0 0 30px rgba(139,53,255,.18);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}

.pomp-contact-links a {
  box-sizing: border-box;
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 12px;
  color: #F8F5FF !important;
  text-decoration: none !important;
  border: 1px solid rgba(255,255,255,.09);
  border-radius: 14px;
  background: rgba(255,255,255,.045);
  font-size: 12px;
  font-weight: 750;
  transition:
    transform .18s ease,
    border-color .18s ease,
    background .18s ease;
}

.pomp-contact-links a:hover {
  transform: translateY(-2px);
  border-color: rgba(139,53,255,.72);
  background: rgba(139,53,255,.16);
}

.pomp-contact-caption {
  padding: 3px 5px 7px;
  color: #C5A9F1;
  font-size: 11px;
  line-height: 1.9;
  text-align: center;
}

.pomp-contact-brand {
  text-align: center;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: .4px;
  background: linear-gradient(
    90deg,
    #B78BFF,
    #72B7FF,
    #FF85D3
  );
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

@media (max-width: 640px) {
  body {
    overflow-x: hidden;
  }

  img,
  video,
  canvas {
    max-width: 100%;
  }

  .pomp-contact-dock {
    right: 12px;
    bottom: max(12px, env(safe-area-inset-bottom));
  }

  .pomp-contact-dock summary {
    padding: 12px 15px;
    font-size: 12px;
  }

  .pomp-contact-links {
    width: min(295px, calc(100vw - 24px));
  }
}

@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }

  .pomp-contact-links a {
    transition: none;
  }
}
"""


# ==========================================================
# OFFICIAL BRAND LOGO
# ==========================================================

LOGO = """<svg xmlns="http://www.w3.org/2000/svg"
viewBox="0 0 240 240">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#8B35FF"/>
    <stop offset="52%" stop-color="#168CFF"/>
    <stop offset="100%" stop-color="#FF3DBB"/>
  </linearGradient>
</defs>
<rect x="7" y="7" width="226" height="226" rx="58"
fill="#050509" stroke="url(#g)" stroke-width="6"/>
<path d="M66 176V64h43c27 0 42 14 42 37s-15 37-42 37H92"
fill="none" stroke="url(#g)" stroke-width="17"
stroke-linecap="round" stroke-linejoin="round"/>
<path d="M151 176V65h12l29 42 29-42h4v111"
fill="none" stroke="#fff" stroke-opacity=".95"
stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


# ==========================================================
# SUPPORT AND OFFICIAL TELEGRAM LINKS
# ==========================================================

CONTACT_MENU = """
<aside class="pomp-contact-dock"
       aria-label="ارتباط با POMP NET MOHAMMAD">
  <details>
    <summary>پشتیبانی و ارتباط</summary>

    <nav class="pomp-contact-links"
         aria-label="لینک‌های رسمی POMP NET">

      <div class="pomp-contact-brand">
        ✦ POMP NET MOHAMMAD 👑
      </div>

      <div class="pomp-contact-caption">
        ارتباط مستقیم با تیم پشتیبانی
      </div>

      <a href="https://t.me/NovaTunneli"
         target="_blank" rel="noopener noreferrer">
        💬 پشتیبانی اصلی — @NovaTunneli
      </a>

      <a href="https://t.me/Kmnbvczx0090"
         target="_blank" rel="noopener noreferrer">
        👑 ارتباط با مستر یوسف — @Kmnbvczx0090
      </a>

      <a href="https://t.me/pompnet"
         target="_blank" rel="noopener noreferrer">
        📢 کانال رسمی پمپ‌نت
      </a>

      <a href="https://t.me/PompNett"
         target="_blank" rel="noopener noreferrer">
        👥 گروه گفت‌وگوی پمپ‌نت
      </a>

      <a href="https://t.me/+UV34C7Ohs9hiZTc0"
         target="_blank" rel="noopener noreferrer">
        🤝 جامعه پمپ‌نت
      </a>

    </nav>
  </details>
</aside>
"""


# ==========================================================
# BRANDING HELPERS
# ==========================================================

BRAND_PATTERNS = [
    r"(?i)Spider\s*Panel\s*v?\d+(?:\.\d+)*",
    r"(?i)Spider\s*Panel",
    r"(?i)SpiderPanel",
]


def replace_brand_names(html: str) -> str:
    """Replace old visible brand names without rebuilding the page."""

    for pattern in BRAND_PATTERNS:
        html = re.sub(pattern, "POMP NET MOHAMMAD", html)

    # Update page title.
    title = (
        "<title>"
        "POMP NET MOHAMMAD 👑 | پنل مدیریت"
        "</title>"
    )

    if re.search(r"<title\b[^>]*>.*?</title>", html, re.I | re.S):
        html = re.sub(
            r"<title\b[^>]*>.*?</title>",
            lambda _: title,
            html,
            count=1,
            flags=re.I | re.S,
        )
    elif re.search(r"</head\s*>", html, re.I):
        html = re.sub(
            r"</head\s*>",
            lambda _: title + "\n</head>",
            html,
            count=1,
            flags=re.I,
        )

    return html


def set_persian_direction(html: str) -> str:
    """Set Persian and RTL attributes without duplicating attributes."""

    match = re.search(r"<html\b([^>]*)>", html, flags=re.I)

    if not match:
        return html

    attrs = match.group(1)

    attrs = re.sub(
        r'\s+(?:lang|dir)\s*=\s*(["\']).*?\1',
        "",
        attrs,
        flags=re.I,
    )

    new_tag = '<html' + attrs + ' lang="fa" dir="rtl">'

    return html[:match.start()] + new_tag + html[match.end():]


def add_styles(html: str) -> str:
    marker = "POMP NET MOHAMMAD | CRYSTAL GLASS"

    if marker in html:
        return html

    style_tag = "\n<style>\n" + CSS + "\n</style>\n"

    if re.search(r"</head\s*>", html, re.I):
        return re.sub(
            r"</head\s*>",
            lambda _: style_tag + "</head>",
            html,
            count=1,
            flags=re.I,
        )

    return style_tag + html


def add_favicon(html: str) -> str:
    if re.search(
        r'<link\b[^>]*rel\s*=\s*["\'](?:shortcut\s+)?icon["\']',
        html,
        flags=re.I,
    ):
        return html

    icon_tag = (
        '<link rel="icon" type="image/svg+xml" '
        'href="/static/pompnet-logo.svg">'
    )

    if re.search(r"</head\s*>", html, re.I):
        return re.sub(
            r"</head\s*>",
            lambda _: icon_tag + "\n</head>",
            html,
            count=1,
            flags=re.I,
        )

    return html


def add_contact_menu(html: str) -> str:
    marker = 'aria-label="لینک‌های رسمی POMP NET"'

    if marker in html:
        return html

    if re.search(r"</body\s*>", html, re.I):
        return re.sub(
            r"</body\s*>",
            lambda _: CONTACT_MENU + "\n</body>",
            html,
            count=1,
            flags=re.I,
        )

    # Keep the page intact if it does not have a body closing tag.
    return html + "\n" + CONTACT_MENU


def process_html(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")

    updated = replace_brand_names(original)
    updated = set_persian_direction(updated)
    updated = add_styles(updated)
    updated = add_favicon(updated)
    updated = add_contact_menu(updated)

    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True

    return False


# ==========================================================
# RUN BRANDING
# ==========================================================

STATIC.mkdir(parents=True, exist_ok=True)

logo_path = STATIC / "pompnet-logo.svg"
logo_path.write_text(LOGO, encoding="utf-8")

for page in HTML_FILES:
    try:
        changed = process_html(page)
        status = "Updated" if changed else "Already branded"
        print(f"{status}: {page.relative_to(ROOT)}")
    except (OSError, UnicodeError) as exc:
        raise SystemExit(
            f"ERROR: Could not update {page.relative_to(ROOT)}: {exc}"
        ) from exc


# ==========================================================
# VERIFY CORE FILES — NEVER REPLACE THE CORE
# ==========================================================

required_files = [
    ROOT / "main.py",
    ROOT / "requirements.txt",
    STATIC / "index.html",
]

missing_files = [
    str(path.relative_to(ROOT))
    for path in required_files
    if not path.is_file()
]

if missing_files:
    raise SystemExit(
        "ERROR: Required files missing: " + ", ".join(missing_files)
    )

print()
print("POMP NET MOHAMMAD branding completed.")
print("Original main.py was not rewritten.")
print("Original API and backend files were preserved.")
print("Support menu and Telegram links were added to HTML pages.")
