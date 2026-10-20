#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
POMP NET MOHAMMAD
پاک‌سازی لینک‌ها و تبلیغات قابل‌مشاهده برند قبلی.
فقط فایل‌های HTML داخل static بررسی می‌شوند.
منطق بک‌اند، API، مسیرها، کاربران و تنظیمات تغییر نمی‌کنند.
"""

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/app").resolve()
STATIC = ROOT / "static"

if not STATIC.is_dir():
    raise SystemExit(
        f"ERROR: پوشه استاتیک پیدا نشد: {STATIC}"
    )

# فقط نشانه‌های تبلیغاتی و برند قبلی؛ نه فایل‌های بک‌اند.
BRAND_WORDS = re.compile(
    r"spider\s*panel|spiderpanel",
    re.IGNORECASE,
)

# لینک‌های صریحاً مربوط به برند قبلی.
OLD_BRAND_URL = re.compile(
    r"(?:spiderpanel|spider-panel)",
    re.IGNORECASE,
)

# لینک‌هایی حذف می‌شوند که متنشان تبلیغ برند قبلی باشد
# یا آدرس آن‌ها صریحاً به همان برند اشاره کند.
ANCHOR = re.compile(
    r"<a\b(?P<attrs>[^>]*)>(?P<body>.*?)</a\s*>",
    re.IGNORECASE | re.DOTALL,
)

def clean_html(html: str) -> str:
    def clean_anchor(match: re.Match) -> str:
        attrs = match.group("attrs")
        body = match.group("body")

        href_match = re.search(
            r"""href\s*=\s*(['"])(.*?)\1""",
            attrs,
            re.IGNORECASE | re.DOTALL,
        )

        href = href_match.group(2) if href_match else ""

        # فقط لینک تبلیغاتی صریح برند قبلی حذف می‌شود.
        if OLD_BRAND_URL.search(href):
            return ""

        # لینک‌هایی که صرفاً برای تبلیغ نام برند قبلی هستند.
        visible_text = re.sub(r"<[^>]+>", " ", body)
        visible_text = re.sub(r"\s+", " ", visible_text).strip()

        if BRAND_WORDS.search(visible_text):
            return ""

        return match.group(0)

    return ANCHOR.sub(clean_anchor, html)


def main() -> None:
    pages = sorted(STATIC.rglob("*.html"))

    if not pages:
        raise SystemExit(
            "ERROR: هیچ فایل HTML برای بررسی پیدا نشد."
        )

    changed = 0

    for page in pages:
        original = page.read_text(encoding="utf-8")
        updated = clean_html(original)

        if updated != original:
            page.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"UPDATED: {page.relative_to(ROOT)}")

    print(f"POMP NET cleanup finished. Changed pages: {changed}")


if __name__ == "__main__":
    main()
