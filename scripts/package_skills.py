#!/usr/bin/env python3
"""Package skills/ mappen naar dist/<name>.skill met validatie."""
from __future__ import annotations
import argparse
import datetime as _dt
import re
import shutil
import sys
import zipfile
from pathlib import Path

REQUIRED_FIELDS = ("name", "description", "version", "last_updated", "author", "license", "jurisdiction", "compatibility", "source")
OPTIONAL_FIELDS = ("compatibility_versions",)
DESC_MIN = 30
DESC_MAX = 500
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEMVER_RANGE_RE = re.compile(r"^(\*|>=?\d+\.\d+(?:\.\d+)?|~\d+\.\d+(?:\.\d+)?|\d+\.\d+(?:\.\d+)?)$")
DISCLAIMER_MARKER = "concept ter beoordeling"
IGNORED_FILES = {".DS_Store", "__pycache__", ".git", "MANIFEST.json"}

class ValidationError(Exception):
    pass

def project_root() -> Path:
    return Path(__file__).resolve().parent.parent

def validate_version(version: str) -> bool:
    return bool(VERSION_RE.match(version.strip()))

def validate_date(date: str) -> bool:
    return bool(DATE_RE.match(date.strip()))


def validate_compatibility_versions(cv: dict) -> list[str]:
    """Valideer compatibility_versions map (platform → semver-range)."""
    errors = []
    if not isinstance(cv, dict):
        return ["compatibility_versions moet een map zijn"]
    for platform, version in cv.items():
        if not isinstance(version, str):
            errors.append(f"compatibility_versions[{platform}] moet een string zijn")
            continue
        if not SEMVER_RANGE_RE.match(version.strip()):
            errors.append(f"compatibility_versions[{platform}]: '{version}' is geen geldige semver-range (zie conventions.md)")
    return errors

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
            elif val.startswith("{") and val.endswith("}"):
                # inline map: {key: val, key2: val2}
                inner = val[1:-1]
                parsed = {}
                for kv in inner.split(","):
                    kv = kv.strip()
                    if not kv:
                        continue
                    if ":" in kv:
                        k, v = kv.split(":", 1)
                        parsed[k.strip().strip('"')] = v.strip().strip('"')
                    else:
                        parsed[kv.strip('"')] = True
                meta[current_key] = parsed
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
    text = skill_md.read_text(encoding="utf-8")
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
    last_updated = str(meta["last_updated"])
    if not validate_date(last_updated):
        errors.append(f"{skill_dir.name}: last_updated is geen YYYY-MM-DD")
    else:
        # P6: last_updated mag niet in de toekomst liggen
        try:
            lu_date = _dt.date.fromisoformat(last_updated)
            if lu_date > _dt.date.today():
                errors.append(f"{skill_dir.name}: last_updated {last_updated} ligt in de toekomst")
        except ValueError:
            errors.append(f"{skill_dir.name}: last_updated {last_updated} is geen geldige datum")
    if not validate_description(str(meta["description"])):
        errors.append(f"{skill_dir.name}: description is <{DESC_MIN} of >{DESC_MAX} tekens")
    # K9: disclaimer moet in SKILL.md staan
    if DISCLAIMER_MARKER not in text:
        errors.append(f"{skill_dir.name}: SKILL.md bevat geen <disclaimer>-blok met '{DISCLAIMER_MARKER}'")
    # K10: compatibility_versions (optioneel) — als aanwezig, moet het een dict zijn + geldige ranges
    cv = meta.get("compatibility_versions")
    if cv is not None:
        if not isinstance(cv, dict):
            errors.append(f"{skill_dir.name}: compatibility_versions moet een map zijn (platform: versie)")
        else:
            cv_errors = validate_compatibility_versions(cv)
            for e in cv_errors:
                errors.append(f"{skill_dir.name}: {e}")
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
    """Returneer skill-mappen.

    Als `only` is opgegeven, returneer een lijst met die ene map (of een lege lijst
    als de map niet bestaat). De caller verwerkt de lege-lijst-case expliciet —
    we returneren nooit een pad dat niet is_dir().
    """
    if only:
        candidate = skills_dir / only
        return [candidate] if candidate.is_dir() else []
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
    if args.skill and not skills:
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
