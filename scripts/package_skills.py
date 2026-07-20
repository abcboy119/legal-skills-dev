#!/usr/bin/env python3
"""Package skills/ mappen naar dist/<name>.skill met validatie."""
from __future__ import annotations
import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

REQUIRED_FIELDS = ("name", "description", "version", "last_updated", "author", "license", "jurisdiction", "compatibility")
DESC_MIN = 30
DESC_MAX = 500
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
IGNORED_FILES = {".DS_Store", "__pycache__", ".git"}

class ValidationError(Exception):
    pass

def project_root() -> Path:
    return Path(__file__).resolve().parent.parent

def validate_version(version: str) -> bool:
    return bool(VERSION_RE.match(version.strip()))

def validate_date(date: str) -> bool:
    return bool(DATE_RE.match(date.strip()))

def validate_description(desc: str) -> bool:
    clean = " ".join(desc.split())
    return DESC_MIN <= len(clean) <= DESC_MAX

def parse_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValidationError(f"{skill_md}: geen frontmatter gevonden")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValidationError(f"{skill_md}: frontmatter niet afgesloten")
    block = parts[1]
    meta = {}
    current_key = None
    current_lines = []
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        m = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if m and not line.startswith((" ", "\t")):
            if current_key is not None:
                meta[current_key] = " ".join(current_lines).strip()
            current_key = m.group(1)
            val = m.group(2).strip()
            if val == ">":
                current_lines = []
            elif val.startswith("[") and val.endswith("]"):
                meta[current_key] = [v.strip() for v in val[1:-1].split(",") if v.strip()]
                current_key = None
                current_lines = []
            elif val:
                meta[current_key] = val
                current_key = None
                current_lines = []
            else:
                current_lines = []
        elif current_key is not None:
            current_lines.append(line.strip())
    if current_key is not None:
        meta[current_key] = " ".join(current_lines).strip()
    if not meta:
        raise ValidationError(f"{skill_md}: lege frontmatter")
    return meta

def validate_skill(skill_dir: Path) -> list[str]:
    errors = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir.name}: SKILL.md ontbreekt"]
    try:
        meta = parse_frontmatter(skill_md)
    except ValidationError as e:
        return [str(e)]
    for field in REQUIRED_FIELDS:
        if field not in meta or not meta[field]:
            errors.append(f"{skill_dir.name}: frontmatter ontbreekt veld '{field}'")
    if errors:
        return errors
    if meta.get("name") != skill_dir.name:
        name_val = meta.get("name", "")
        errors.append(f"{skill_dir.name}: name '{name_val}' komt niet overeen met mapnaam")
    if not validate_version(str(meta["version"])):
        errors.append(f"{skill_dir.name}: version is geen semver")
    if not validate_date(str(meta["last_updated"])):
        errors.append(f"{skill_dir.name}: last_updated is geen YYYY-MM-DD")
    if not validate_description(str(meta["description"])):
        errors.append(f"{skill_dir.name}: description is <{DESC_MIN} of >{DESC_MAX} tekens")
    for sub in ("references", "assets"):
        subdir = skill_dir / sub
        if subdir.is_dir():
            content = [f for f in subdir.iterdir() if f.is_file() and f.name not in IGNORED_FILES]
            if not content:
                errors.append(f"{skill_dir.name}: {sub}/ bestaat maar is leeg")
    return errors

def package_skill(skill_dir: Path, dist_dir: Path) -> Path:
    dist_dir.mkdir(parents=True, exist_ok=True)
    out = dist_dir / f"{skill_dir.name}.skill"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(skill_dir.rglob("*")):
            if path.is_dir():
                continue
            if any(part in IGNORED_FILES for part in path.parts):
                continue
            z.write(path, path.relative_to(skill_dir))
    return out

def iter_skills(skills_dir: Path, only: str | None) -> list[Path]:
    if only:
        return [skills_dir / only]
    return sorted([p for p in skills_dir.iterdir() if p.is_dir()])

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", nargs="?", help="optionele skill-naam")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    root = project_root()
    skills_dir = root / "skills"
    dist_dir = root / "dist"

    if args.clean and dist_dir.exists():
        shutil.rmtree(dist_dir)
        print(f"Cleaned {dist_dir}")

    if not skills_dir.is_dir():
        print(f"Geen skills/-map gevonden op {skills_dir}", file=sys.stderr)
        return 1

    skills = iter_skills(skills_dir, args.skill)
    if args.skill and not skills[0].is_dir():
        print(f"Skill '{args.skill}' niet gevonden in {skills_dir}", file=sys.stderr)
        return 1

    failed = 0
    for skill_dir in skills:
        errors = validate_skill(skill_dir)
        if errors:
            failed += 1
            for e in errors:
                print(f"✗ {e}", file=sys.stderr)
            continue
        if args.validate_only:
            print(f"✓ {skill_dir.name} (valid)")
            continue
        out = package_skill(skill_dir, dist_dir)
        meta = parse_frontmatter(skill_dir / "SKILL.md")
        version_val = meta.get("version", "")
        print(f"✓ {skill_dir.name:<22} {version_val:<7} → {out.relative_to(root)}")

    if args.validate_only:
        print(f"{len(skills) - failed}/{len(skills)} skills valid.")
    elif failed == 0:
        print(f"{len(skills)} skills packaged.")
    if failed:
        print(f"{failed} skills failed. Zie bovenstaande fouten.", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
