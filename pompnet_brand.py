#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/app").resolve()
STATIC = ROOT / "static"

REQUIRED_FILES = [
    ROOT / "main.py",
    ROOT / "requirements.txt",
    STATIC / "index.html",
    STATIC / "login.html",
    STATIC / "sub.html",
]

for file_path in REQUIRED_FILES:
    if not file_path.is_file():
        raise SystemExit(
            f"BUILD CHECK FAILED: required file missing: {file_path}"
        )

HTML_FILES = sorted(STATIC.rglob("*.html"))

if not HTML_FILES:
    raise SystemExit("BUILD CHECK FAILED: no HTML files found")

BRAND = "POMP NET MOHAMMAD 👑"

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800;900&display=swap');

:root {
  color-scheme: dark;
  --pomp-bg: #050509;
  --pomp-purple: #8B35FF;
  --pomp-blue: #168CFF;
  --pomp-pink: #FF3DBB;
  --pomp-text: #F8F5FF;
  --pomp-muted: #B7A9CC;
  --pomp-border: rgba(139, 53, 255, .35);
  --pomp-glass: rgba(15, 11, 26, .88);
}

html {
  background: var(--pomp-bg);
  scroll-behavior: smooth;
}

body {
  background-color: var(--pomp-bg);
  color: var(--pomp-text);
  font-family: Vazirmatn, Tahoma, sans-serif;
  -webkit-tap-highlight-color: transparent;
}

button, input, select, textarea {
  font-family: inherit;
}

:where(.card, .panel, .glass, [class*="card"], [class*="panel"]) {
  border-color: var(--pomp-border);
}

input, select, textarea {
  border-color: var(--pomp-border);
}

::selection {
  color: white;
  background: rgba(139, 53, 255, .7);
}

.pomp-contact-dock {
  position: fixed;
  z-index: 99990;
  right: max(12px, env(safe-area-inset-right));
  bottom: max(12px, env(safe-area-inset-bottom));
  direction: rtl;
  font-family: Vazirmatn, Tahoma, sans-serif;
}

.pomp-contact-dock summary {
  list-style: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  color: #fff;
  font-size: 13px;
  font-weight: 900;
  border: 1px solid rgba(255,255,255,.25);
  border-radius: 999px;
  background: linear-gradient(
    125deg,
    var(--pomp-purple),
    var(--pomp-blue),
    var(--pomp-pink)
  );
  box-shadow: 0 8px 30px rgba(139,53,255,.3);
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
  position: absolute;
  right: 0;
  bottom: calc(100% + 10px);
  display: grid;
  gap: 9px;
  width: min(310px, calc(100vw - 24px));
  padding: 14px;
  border: 1px solid var(--pomp-border);
  border-radius: 22px;
  background: rgba(8,7,16,.97);
  box-shadow: 0 18px 55px rgba(0,0,0,.55);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}

.pomp-contact-brand {
  color: #d8baff;
  text-align: center;
  font-weight: 900;
  padding: 5px;
}

.pomp-contact-caption {
  color: var(--pomp-muted);
  text-align: center;
  font-size: 11px;
  padding: 3px 4px 7px;
}

.pomp-contact-links a {
  box-sizing: border-box;
  display: block;
  padding: 12px;
  color: #fff !important;
  text-decoration: none !important;
  border: 1px solid rgba(255,255,255,.09);
  border-radius: 14px;
  background: rgba(255,255,255,.045);
  font-size: 12px;
  font-weight: 700;
}

.pomp-contact-links a:hover {
  border-color: var(--pomp-purple);
  background: rgba(139,53,255,.16);
}

@media (max-width: 640px) {
  body {
    overflow-x: hidden;
  }

  .pomp-contact-links {
    width: min(290px, calc(100vw - 24px));
  }
}

@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }
}
"""

LOGO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240">
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
fill="none" stroke="#fff" stroke-width="8"
stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

CONTACT_MENU = """
<aside class="pomp-contact-dock"
       aria-label="ارتباط با POMP NET MOHAMMAD">
  <details>
    <summary>پشتیبانی و ارتباط</summary>
    <nav class="pomp-contact-links"
         aria-label="لینک‌های رسمی POMP NET">
      <div class="pomp-contact-brand">✦ POMP NET MOHAMMAD 👑</div>
      <div class="pomp-contact-caption">راه‌های ارتباطی رسمی</div>
      <a href="https://t.me/NovaTunneli"
         target="_blank" rel="noopener noreferrer">
        💬 پشتیبانی — @NovaTunneli
      </a>
      <a href="https://t.me/Kmnbvczx0090"
         target="_blank" rel="noopener noreferrer">
        👑 مستر یوسف — @Kmnbvczx0090
      </a>
      <a href="https://t.me/pompnet"
         target="_blank" rel="noopener noreferrer">
        📢 کانال رسمی پمپ‌نت
      </a>
      <a href="https://t.me/PompNett"
         target="_blank" rel="noopener noreferrer">
        👥 گروه پمپ‌نت
      </a>
      <a href="https://t.me/+UV34C7Ohs9hiZTc0"
         target="_blank" rel="noopener noreferrer">
        🤝 جامعه پمپ‌نت
      </a>
    </nav>
  </details>
</aside>
"""

# نام‌های نمایشی شناخته‌شده؛ این جایگزینی جایگزین بررسی کل پروژه نیست.
BRAND_PATTERNS = [
    r"(?i)Spider\s*Panel\s*v?\d+(?:\.\d+)*",
    r"(?i)Spider\s*Panel",
    r"(?i)SpiderPanel",
    r"(?i)SPiDER\s+PANEL",
]


def replace_visible_brand(html: str) -> str:
    for pattern in BRAND_PATTERNS:
        html = re.sub(pattern, "POMP NET MOHAMMAD", html)

    # نام صفحه را به برند اختصاصی تغییر می‌دهد.
    title = f"<title>{BRAND} | پنل مدیریت</title>"
    title_pattern = r"<title\b[^>]*>.*?</title>"

    if re.search(title_pattern, html, re.I | re.S):
        html = re.sub(
            title_pattern,
            lambda _: title,
            html,
            count=1,
            flags=re.I | re.S,
        )

    return html


def set_persian_rtl(html: str) -> str:
    match = re.search(r"<html\b([^>]*)>", html, re.I)

    if not match:
        return html

    attrs = match.group(1)
    attrs = re.sub(
        r"""\s+(?:lang|dir)\s*=\s*(?:"[^"]*"|'[^']*')""",
        "",
        attrs,
        flags=re.I,
    )

    new_tag = f'<html{attrs} lang="fa" dir="rtl">'
    return html[:match.start()] + new_tag + html[match.end():]


def inject_once(html: str, marker: str, snippet: str) -> str:
    if marker in html:
        return html

    if re.search(r"</head\s*>", html, re.I):
        return re.sub(
            r"</head\s*>",
            lambda _: snippet + "\n</head>",
            html,
            count=1,
            flags=re.I,
        )

    return html


def add_branding(html: str) -> str:
    html = replace_visible_brand(html)
    html = set_persian_rtl(html)

    if "POMP NET MOHAMMAD | CRYSTAL GLASS" not in html:
        html = inject_once(
            html,
            "POMP NET MOHAMMAD | CRYSTAL GLASS",
            "\n<style>\n/* POMP NET MOHAMMAD | CRYSTAL GLASS */\n"
            + CSS
            + "\n</style>\n",
        )

    if not re.search(
        r"""<link\b[^>]*rel=["'](?:shortcut\s+)?icon["']""",
        html,
        re.I,
    ):
        html = inject_once(
            html,
            "pompnet-logo.svg",
            '<link rel="icon" type="image/svg+xml" '
            'href="/static/pompnet-logo.svg">',
        )

    marker = 'aria-label="لینک‌های رسمی POMP NET"'
    if marker not in html:
        if re.search(r"</body\s*>", html, re.I):
            html = re.sub(
                r"</body\s*>",
                lambda _: CONTACT_MENU + "\n</body>",
                html,
                count=1,
                flags=re.I,
            )
        else:
            html += "\n" + CONTACT_MENU

    return html


def main() -> None:
    logo_path = STATIC / "pompnet-logo.svg"
    logo_path.write_text(LOGO, encoding="utf-8")

    for page in HTML_FILES:
        original = page.read_text(encoding="utf-8")
        updated = add_branding(original)

        if updated != original:
            page.write_text(updated, encoding="utf-8")
            print(f"BRANDED: {page.relative_to(ROOT)}")
        else:
            print(f"UNCHANGED: {page.relative_to(ROOT)}")

    # کنترل نهایی وجود فایل‌های حیاتی؛ هیچ‌کدام بازنویسی نمی‌شوند.
    for file_path in REQUIRED_FILES:
        if not file_path.is_file():
            raise SystemExit(
                f"BUILD CHECK FAILED: {file_path} disappeared"
            )

    print("POMP NET MOHAMMAD branding step completed.")
    print("Core application and requirements were not rewritten.")


if __name__ == "__main__":
    main()
