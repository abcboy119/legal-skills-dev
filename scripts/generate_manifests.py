#!/usr/bin/env python3
"""Genereer of verifieer references/MANIFEST.json-bestanden met SHA-256 hashes.

Gebruik:
    python3 scripts/generate_manifests.py              # genereer alle MANIFEST.json
    python3 scripts/generate_manifests.py --check      # verifieer dat bestaande hashes kloppen
    python3 scripts/generate_manifests.py documenten-audit  # enkele skill

Het MANIFEST.json-bestand wordt door package_skills.py genegeerd (in IGNORED_FILES)
en niet meegenomen in de .skill-zip. Het dient uitsluitend om stille wijzigingen
aan references/assets te detecteren zonder dat de SKILL.md version hoeft te worden
gebumpt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

IGNORED = {".DS_Store", "__pycache__", ".git", "MANIFEST.json"}


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def iter_skill_files(skill_dir: Path) -> list[Path]:
    """Alle bestanden in references/ en assets/, behalve MANIFEST.json en IGNORED."""
    files = []
    for sub in ("references", "assets"):
        subdir = skill_dir / sub
        if not subdir.is_dir():
            continue
        for p in sorted(subdir.rglob("*")):
            if p.is_file() and p.name not in IGNORED:
                files.append(p)
    return files


def generate_manifest(skill_dir: Path) -> dict:
    files = iter_skill_files(skill_dir)
    return {
        "skill": skill_dir.name,
        "generated_at": date.today().isoformat(),
        "files": [
            {
                "path": str(p.relative_to(skill_dir)),
                "sha256": sha256_of(p),
            }
            for p in files
        ],
    }


def write_manifest(skill_dir: Path) -> Path:
    manifest = generate_manifest(skill_dir)
    out = skill_dir / "references" / "MANIFEST.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def check_manifest(skill_dir: Path) -> list[str]:
    """Return lijst van mismatches (lege lijst = OK)."""
    manifest_path = skill_dir / "references" / "MANIFEST.json"
    if not manifest_path.exists():
        return [f"{skill_dir.name}: references/MANIFEST.json ontbreekt — draai generate_manifests.py"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    actual_files = iter_skill_files(skill_dir)
    actual_paths = {str(p.relative_to(skill_dir)) for p in actual_files}
    manifest_paths = {f["path"] for f in manifest["files"]}

    errors = []
    # Missende bestanden (wel op schijf, niet in manifest)
    for p in actual_paths - manifest_paths:
        errors.append(f"{skill_dir.name}: {p} op schijf maar niet in MANIFEST.json")
    # Extra bestanden (wel in manifest, niet op schijf)
    for p in manifest_paths - actual_paths:
        errors.append(f"{skill_dir.name}: {p} in MANIFEST.json maar niet op schijf")
    # Hash mismatches
    for f in manifest["files"]:
        p = skill_dir / f["path"]
        if not p.exists():
            continue  # al gemeld hierboven
        actual = sha256_of(p)
        if actual != f["sha256"]:
            errors.append(
                f"{skill_dir.name}: {f['path']} hash mismatch "
                f"(manifest={f['sha256'][:12]}…, actual={actual[:12]}…) — draai generate_manifests.py"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", nargs="?", help="optionele skill-naam")
    parser.add_argument("--check", action="store_true", help="verifieer in plaats van genereer")
    args = parser.parse_args()

    root = project_root()
    skills_dir = root / "skills"

    if not skills_dir.is_dir():
        print(f"Geen skills/-map gevonden op {skills_dir}", file=sys.stderr)
        return 1

    if args.skill:
        candidate = skills_dir / args.skill
        if not candidate.is_dir():
            print(f"Skill '{args.skill}' niet gevonden", file=sys.stderr)
            return 1
        skills = [candidate]
    else:
        skills = sorted([p for p in skills_dir.iterdir() if p.is_dir()])

    failed = 0
    for skill_dir in skills:
        if args.check:
            errors = check_manifest(skill_dir)
            if errors:
                failed += 1
                for e in errors:
                    print(f"✗ {e}", file=sys.stderr)
            else:
                print(f"✓ {skill_dir.name} (manifest consistent)")
        else:
            out = write_manifest(skill_dir)
            manifest = json.loads(out.read_text(encoding="utf-8"))
            print(f"✓ {skill_dir.name:<22} {len(manifest['files'])} bestanden → {out.relative_to(root)}")

    if args.check and failed:
        print(f"\n{failed} skills met inconsistente manifesten.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
