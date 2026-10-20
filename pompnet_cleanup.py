#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
POMP NET MOHAMMAD
Safe frontend branding and cleanup.

- Fixes the HTML regex capture-group crash.
- Preserves backend code, API routes and application logic.
- Updates branding only in HTML files.
- Keeps existing HTML attributes except lang and dir.
- Adds the POMP NET glass theme when needed.
"""

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/app").resolve()
STATIC = ROOT / "static"

BRAND = "POMP NET MOHAMMAD"
STYLE_MARKER = "POMP NET MOHAMMAD — CRYSTAL GLASS"

GLASS_CSS = r"""
/* POMP NET MOHAMMAD — CRYSTAL GLASS */
:root {
  color-scheme: dark;
  --pomp-bg: #050509;
  --pomp-purple: #8B35FF;
  --pomp-blue: #168CFF;
  --pomp-pink: #FF3DBB;
  --pomp-text: #F8F5FF;
  --pomp-muted: #B7A9CC;
  --pomp-border: rgba(139, 53, 255, .38);
  --pomp-glass: rgba(15, 11, 26, .86);
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

::selection {
  background: var(--pomp-purple);
  color: #fff;
}

@media (max-width: 640px) {
  body {
    overflow-x: hidden;
  }
}
"""

OLD_BRAND = re.compile(
    r"spider\s*panel(?:\s*v?\d+(?:\.\d+)*)?|spiderpanel",
    re.IGNORECASE,
)


def log(status, message):
    print(f"[{status}] {message}", flush=True)


def fix_html_attributes(html):
    """Set Persian RTL without deleting other HTML attributes."""

    def replace_tag(match):
        # Use group(0): the complete match always exists.
        tag = match.group(0)
        opening = tag[:-1] if tag.endswith(">") else tag

        opening = re.sub(
            r"""\s+(?:lang|dir)\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)""",
            "",
            opening,
            flags=re.IGNORECASE,
        )

        return opening + ' lang="fa" dir="rtl">'

    return re.sub(
        r"<html\b[^>]*>",
        replace_tag,
        html,
        count=1,
        flags=re.IGNORECASE,
    )


def fix_title(html):
    title = f"<title>{BRAND} | پنل مدیریت</title>"

    pattern = r"<title\b[^>]*>.*?</title\s*>"

    if re.search(pattern, html, flags=re.IGNORECASE | re.DOTALL):
        return re.sub(
            pattern,
            lambda _: title,
            html,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )

    if re.search(r"</head\s*>", html, flags=re.IGNORECASE):
        return re.sub(
            r"</head\s*>",
            lambda _: title + "\n</head>",
            html,
            count=1,
            flags=re.IGNORECASE,
        )

    return html


def inject_theme(html):
    if STYLE_MARKER in html:
        return html

    if not re.search(r"</head\s*>", html, flags=re.IGNORECASE):
        log("WARN", "تگ </head> پیدا نشد؛ CSS در این صفحه اضافه نشد.")
        return html

    style = "<style>\n" + GLASS_CSS + "\n</style>\n"

    return re.sub(
        r"</head\s*>",
        lambda _: style + "</head>",
        html,
        count=1,
        flags=re.IGNORECASE,
    )


def clean_html(html):
    # Replace visible branding in HTML only.
    # Do not rewrite JavaScript, CSS, APIs or backend files.
    html = OLD_BRAND.sub(BRAND, html)

    html = fix_html_attributes(html)
    html = fix_title(html)
    html = inject_theme(html)

    return html


def main():
    print("=" * 58)
    print("POMP NET MOHAMMAD — SAFE FRONTEND REPAIR")
    print("=" * 58)

    if not ROOT.is_dir():
        log("FAIL", f"مسیر پروژه پیدا نشد: {ROOT}")
        raise SystemExit(1)

    if not STATIC.is_dir():
        log("FAIL", f"پوشه رابط کاربری پیدا نشد: {STATIC}")
        raise SystemExit(1)

    files = [
        path
        for path in STATIC.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".html", ".htm"}
    ]

    if not files:
        log("FAIL", "هیچ فایل HTML برای بررسی پیدا نشد.")
        raise SystemExit(1)

    changed = 0
    failed = 0

    for path in files:
        try:
            original = path.read_text(encoding="utf-8")
            updated = clean_html(original)

            if updated != original:
                path.write_text(updated, encoding="utf-8")
                changed += 1
                log("UPDATED", str(path.relative_to(ROOT)))
            else:
                log("PASS", str(path.relative_to(ROOT)))

        except (OSError, UnicodeError, re.error) as error:
            failed += 1
            log("FAIL", f"{path.relative_to(ROOT)}: {error}")

    # Validate required project files without changing them.
    required = [
        ROOT / "main.py",
        ROOT / "requirements.txt",
        ROOT / "static" / "index.html",
        ROOT / "static" / "login.html",
        ROOT / "static" / "sub.html",
    ]

    missing = []

    for path in required:
        if path.is_file() and path.stat().st_size > 0:
            log("PASS", f"وجود فایل {path.relative_to(ROOT)}")
        else:
            missing.append(str(path.relative_to(ROOT)))
            log("FAIL", f"فایل ضروری مفقود یا خالی است: {path}")

    print()
    print(f"HTML files scanned: {len(files)}")
    print(f"HTML files changed: {changed}")
    print(f"File processing errors: {failed}")

    if missing or failed:
        log("FAIL", "بررسی ناموفق بود؛ خطاهای بالا باید بررسی شوند.")
        raise SystemExit(1)

    print("PASS: Cleanup completed.")
    print(
        "توجه: این موفقیت به معنی موفقیت Docker، "
        "اجرای برنامه یا Deploy نیست."
    )


if __name__ == "__main__":
    main()
