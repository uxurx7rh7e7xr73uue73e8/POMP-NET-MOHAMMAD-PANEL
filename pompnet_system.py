#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
POMP NET MOHAMMAD
System branding and safe source audit.

این اسکریپت ابتدا فایل‌های متنی را بررسی می‌کند.
به‌صورت پیش‌فرض هیچ فایلی را تغییر نمی‌دهد.
"""

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/app").resolve()

BRAND = "POMP NET MOHAMMAD"

# پوشه‌هایی که ممکن است شامل کد اجرایی یا اطلاعات حساس باشند،
# به‌صورت پیش‌فرض دست‌کاری نمی‌شوند.
EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "site-packages",
}

TEXT_EXTENSIONS = {
    ".py",
    ".html",
    ".htm",
    ".css",
    ".js",
    ".mjs",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".ini",
    ".conf",
    ".service",
    ".sh",
    ".md",
    ".txt",
    ".xml",
    ".svg",
}

# فقط برای پیدا کردن موارد احتمالی برند قدیمی است.
# این عبارت‌ها به‌صورت خودکار جایگزین نمی‌شوند.
OLD_BRAND = re.compile(
    r"spider\s*panel|spiderpanel|spider-panel",
    re.IGNORECASE,
)

def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def main():
    if not ROOT.is_dir():
        raise SystemExit(f"ERROR: مسیر پروژه پیدا نشد: {ROOT}")

    scanned = 0
    matches = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if should_skip(path):
            continue

        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        scanned += 1

        for number, line in enumerate(content.splitlines(), start=1):
            if OLD_BRAND.search(line):
                relative = path.relative_to(ROOT)
                matches.append((str(relative), number, line.strip()))

    print("=" * 56)
    print(f" {BRAND} — SYSTEM BRAND AUDIT")
    print("=" * 56)
    print(f"Root: {ROOT}")
    print(f"Text files scanned: {scanned}")
    print(f"Old-brand references: {len(matches)}")
    print()

    for filename, number, line in matches:
        print(f"{filename}:{number}: {line[:240]}")

    print()
    print("AUDIT FINISHED")
    print("هیچ فایلی تغییر نکرد.")
    print("موارد پیدا شده باید بر اساس نقششان بررسی شوند.")
    print("نام‌های داخلی، APIها و مسیرهای اجرایی را کورکورانه تغییر نده.")


if __name__ == "__main__":
    main()
