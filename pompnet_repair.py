#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
POMP NET MOHAMMAD
Safe project repair and validation.

Usage:
    python pompnet_repair.py /app

This script:
- Backs up files before modifying them.
- Fixes the known HTML regex group error.
- Validates required project files.
- Compiles Python source files.
- Checks CSS presence and Docker integration.
- Does not blindly rename internal APIs or routes.
"""

from pathlib import Path
import re
import shutil
import sys
import py_compile
import tempfile
import time

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

BACKUP_DIR = ROOT / ".pompnet-backup"

REQUIRED_FILES = [
    "Dockerfile",
    "main.py",
    "requirements.txt",
    "railway.toml",
    "pompnet_brand.py",
    "pompnet_cleanup.py",
]

def report(status, message):
    print(f"[{status}] {message}")


def backup_file(path):
    relative = path.relative_to(ROOT)
    destination = BACKUP_DIR / relative
    destination.parent.mkdir(parents=True, exist_ok=True)

    if not destination.exists():
        shutil.copy2(path, destination)


def fix_cleanup_script(path):
    if not path.is_file():
        report("FAIL", "pompnet_cleanup.py پیدا نشد")
        return False

    original = path.read_text(encoding="utf-8")
    updated = original

    # The old regex had no capture group, but the callback
    # accessed match.group(1). Add the required capture group.
    old_pattern = 'r"<html\\b[^>]*>"'
    new_pattern = 'r"(<html\\b[^>]*)>"'

    if old_pattern in updated:
        updated = updated.replace(
            old_pattern,
            new_pattern,
            1,
        )

    if updated != original:
        backup_file(path)
        path.write_text(updated, encoding="utf-8")
        report("FIXED", "خطای گروه regex در pompnet_cleanup.py اصلاح شد")
    else:
        report(
            "INFO",
            "الگوی قدیمی پیدا نشد؛ فایل برای اصلاح خودکار تغییر نکرد",
        )

    try:
        compile(updated, str(path), "exec")
        report("PASS", "ساختار نحوی pompnet_cleanup.py صحیح است")
        return True
    except SyntaxError as error:
        report("FAIL", f"خطای نحوی cleanup: {error}")
        return False


def validate_required_files():
    ok = True

    for name in REQUIRED_FILES:
        path = ROOT / name

        if path.is_file() and path.stat().st_size > 0:
            report("PASS", f"فایل {name} موجود است")
        else:
            report("FAIL", f"فایل {name} وجود ندارد یا خالی است")
            ok = False

    return ok


def compile_python_files():
    ok = True

    excluded = {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
        ".pompnet-backup",
    }

    files = []

    for path in ROOT.rglob("*.py"):
        if any(part in excluded for part in path.parts):
            continue

        files.append(path)

    for path in files:
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
            report("PASS", f"Syntax: {path.relative_to(ROOT)}")
        except (SyntaxError, UnicodeDecodeError, OSError) as error:
            report("FAIL", f"{path.relative_to(ROOT)}: {error}")
            ok = False

    return ok


def validate_css_and_docker():
    dockerfile = ROOT / "Dockerfile"
    css = ROOT / "pompnet.css"
    static = ROOT / "static"

    ok = True

    if not css.is_file():
        report("FAIL", "فایل pompnet.css پیدا نشد")
        ok = False
    else:
        report("PASS", "فایل pompnet.css موجود است")

    if not static.is_dir():
        report("WARN", "پوشه static پیدا نشد")
        ok = False
    else:
        report("PASS", "پوشه static موجود است")

    if dockerfile.is_file():
        text = dockerfile.read_text(encoding="utf-8")

        if "COPY pompnet_cleanup.py" in text:
            if not (ROOT / "pompnet_cleanup.py").is_file():
                report(
                    "FAIL",
                    "Dockerfile فایل cleanup را کپی می‌کند اما فایل وجود ندارد",
                )
                ok = False

        if "COPY pompnet.css" not in text:
            report(
                "WARN",
                "Dockerfile فایل CSS را مستقیماً کپی نمی‌کند؛ "
                "اتصال واقعی CSS باید بررسی شود",
            )

        if "EXPOSE 8080" in text:
            report("PASS", "پورت 8080 در Dockerfile اعلام شده است")
        else:
            report("WARN", "EXPOSE 8080 در Dockerfile پیدا نشد")

    return ok


def main():
    print("=" * 60)
    print("POMP NET MOHAMMAD — SAFE REPAIR")
    print("=" * 60)
    print(f"Project: {ROOT}")
    print()

    if not ROOT.is_dir():
        report("FAIL", "مسیر پروژه معتبر نیست")
        raise SystemExit(1)

    required_ok = validate_required_files()

    cleanup_ok = fix_cleanup_script(
        ROOT / "pompnet_cleanup.py"
    )

    python_ok = compile_python_files()

    integration_ok = validate_css_and_docker()

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    report(
        "PASS" if required_ok else "FAIL",
        "بررسی فایل‌های ضروری",
    )
    report(
        "PASS" if cleanup_ok else "FAIL",
        "بررسی اسکریپت پاک‌سازی",
    )
    report(
        "PASS" if python_ok else "FAIL",
        "بررسی ساختار نحوی فایل‌های Python",
    )
    report(
        "PASS" if integration_ok else "FAIL",
        "بررسی اولیه CSS و Docker",
    )

    print()
    print(
        "این گزارش به‌تنهایی موفقیت Docker Build، "
        "اجرای برنامه یا Deploy را اثبات نمی‌کند."
    )

    if not all([
        required_ok,
        cleanup_ok,
        python_ok,
        integration_ok,
    ]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
