#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
POMP NET MOHAMMAD
Frontend branding cleanup.
فقط فایل‌های متنی رابط کاربری را بررسی می‌کند.
"""

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/app").resolve()
STATIC = ROOT / "static"

BRAND = "POMP NET MOHAMMAD"

EXTENSIONS = {
    ".html", ".htm", ".css", ".js", ".mjs", ".svg"
}

OLD_BRAND = re.compile(
    r"spider\s*panel(?:\s*v?\d+(?:\.\d+)*)?|spiderpanel",
    re.IGNORECASE,
)

OLD_BRAND_URL = re.compile(
    r"""https?://[^\s"'<>)]*(?:spiderpanel|spider-panel)[^\s"'<>)]*""",
    re.IGNORECASE,
)

COLORS = r"""
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
  color: white;
}

@media (max-width: 640px) {
  body {
    overflow-x: hidden;
  }
}
"""

def clean_html(text: str) -> str:
    # حذف لینک‌هایی که مستقیماً به برند قبلی اشاره می‌کنند.
    def remove_old_anchor(match):
        anchor = match.group(0)

        if OLD_BRAND.search(anchor):
            if re.search(
                r"""href\s*=\s*(['"])[^'"]*(?:spiderpanel|spider-panel)[^'"]*\1""",
                anchor,
                re.IGNORECASE,
            ):
                return ""

        return anchor

    text = re.sub(
        r"<a\b[^>]*>.*?</a\s*>",
        remove_old_anchor,
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # جایگزینی نام برند در متن رابط کاربری.
    text = OLD_BRAND.sub(BRAND, text)

    # اصلاح عنوان صفحه.
    title = f"<title>{BRAND} 👑 | پنل مدیریت</title>"

    if re.search(r"</title\s*>", text, re.IGNORECASE):
        text = re.sub(
            r"<title\b[^>]*>.*?</title\s*>",
            title,
            text,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )

    # تنظیم زبان و جهت صفحه بدون حذف سایر ویژگی‌های html.
    def fix_html_tag(match):
        attrs = re.sub(
            r"""\s+(?:lang|dir)\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)""",
            "",
            match.group(1),
            flags=re.IGNORECASE,
        )
        return attrs + ' lang="fa" dir="rtl">'

    text = re.sub(
        r"<html\b[^>]*>",
        fix_html_tag,
        text,
        count=1,
        flags=re.IGNORECASE,
    )

    # افزودن قالب اختصاصی فقط یک بار.
    marker = "POMP NET MOHAMMAD — CRYSTAL GLASS"

    if marker not in text and re.search(
        r"</head\s*>", text, re.IGNORECASE
    ):
        text = re.sub(
            r"</head\s*>",
            lambda _: "<style>\n" + COLORS + "\n</style>\n</head>",
            text,
            count=1,
            flags=re.IGNORECASE,
        )

    return text


def main():
    if not STATIC.is_dir():
        raise SystemExit(
            f"ERROR: پوشه رابط کاربری پیدا نشد: {STATIC}"
        )

    files = [
        path
        for path in STATIC.rglob("*")
        if path.is_file()
        and path.suffix.lower() in EXTENSIONS
    ]

    if not files:
        raise SystemExit(
            "ERROR: هیچ فایل متنی رابط کاربری پیدا نشد."
        )

    changed = 0

    for path in files:
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            print(f"SKIPPED: {path.relative_to(ROOT)}")
            continue

        updated = original

        if path.suffix.lower() in {".html", ".htm"}:
            updated = clean_html(updated)
        else:
            # پاک‌سازی نام برند از فایل‌های متنی رابط کاربری.
            updated = OLD_BRAND.sub(BRAND, updated)

        updated = OLD_BRAND_URL.sub("", updated)

        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"UPDATED: {path.relative_to(ROOT)}")

    print()
    print("POMP NET MOHAMMAD cleanup finished.")
    print(f"Scanned files: {len(files)}")
    print(f"Changed files: {changed}")
    print("توجه: فایل‌های backend و مسیرهای API تغییر نکرده‌اند.")


if __name__ == "__main__":
    main()
