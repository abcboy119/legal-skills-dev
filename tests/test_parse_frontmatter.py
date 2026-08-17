#!/usr/bin/env python3
"""Unit tests voor parse_frontmatter() in package_skills.py.

Deze tests verifiëren de YAML-frontmatter parser onafhankelijk van de
integratietests. Ze coveren edge cases die niet via subprocess worden
getest.

Draaien:
    python3 tests/test_parse_frontmatter.py
of:
    python3 -m pytest tests/test_parse_frontmatter.py -v
"""
from __future__ import annotations
import sys
import tempfile
from pathlib import Path

# Voeg scripts/ toe aan path voor import
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import package_skills as ps

PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {detail}")


def test_minimal_frontmatter() -> None:
    """Test minimaal geldige frontmatter."""
    print("\n[1] Minimale frontmatter met alle verplichte velden")
    content = """---
name: test-skill
description: Dit is een test beschrijving met genoeg tekst.
version: 1.0.0
last_updated: 2026-01-01
author: Test Author
license: CC-BY-4.0
jurisdiction: NL
compatibility: [ClaudeCode]
source: docs/workflow.md
---
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        f.flush()
        path = Path(f.name)

    try:
        meta = ps.parse_frontmatter(path)
        check("name geparseerd", meta.get("name") == "test-skill")
        check("version geparseerd", meta.get("version") == "1.0.0")
        check("description met spaties behouden", "test beschrijving" in meta.get("description", ""))
    finally:
        path.unlink()


def test_inline_list() -> None:
    """Test inline YAML list parsing."""
    print("\n[2] Inline list parsing [platform1, platform2]")
    content = """---
name: list-test
description: Test skill voor list parsing.
version: 1.0.0
last_updated: 2026-01-01
author: Test
license: MIT
jurisdiction: NL
compatibility: [ClaudeCode, OpenCode, ClaudeDesktop]
source: docs/workflow.md
---
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        f.flush()
        path = Path(f.name)

    try:
        meta = ps.parse_frontmatter(path)
        check("compatibility is list", isinstance(meta.get("compatibility"), list))
        check("3 platforms", len(meta.get("compatibility", [])) == 3)
        check("ClaudeCode aanwezig", "ClaudeCode" in meta.get("compatibility", []))
    finally:
        path.unlink()


def test_inline_map() -> None:
    """Test inline YAML map parsing {key: val}."""
    print("\n[3] Inline map parsing {claudeCode: >=1.0}")
    content = """---
name: map-test
description: Test skill voor map parsing met voldoende tekst.
version: 1.0.0
last_updated: 2026-01-01
author: Test
license: MIT
jurisdiction: NL
compatibility: [ClaudeCode]
compatibility_versions: {claudeCode: ">=1.0", openCode: ">=0.5"}
source: docs/workflow.md
---
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        f.flush()
        path = Path(f.name)

    try:
        meta = ps.parse_frontmatter(path)
        check("compatibility_versions is dict", isinstance(meta.get("compatibility_versions"), dict))
        check("claudeCode key", "claudeCode" in meta.get("compatibility_versions", {}))
        check("openCode key", "openCode" in meta.get("compatibility_versions", {}))
    finally:
        path.unlink()


def test_multiline_description() -> None:
    """Test multi-line description met > syntax."""
    print("\n[4] Multi-line description via > syntax")
    content = """---
name: multiline-test
description: >
  Dit is een lange beschrijving die
  over meerdere regels loopt en wordt
  samengevoegd tot één regel.
version: 1.0.0
last_updated: 2026-01-01
author: Test
license: MIT
jurisdiction: NL
compatibility: [ClaudeCode]
source: docs/workflow.md
---
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        f.flush()
        path = Path(f.name)

    try:
        meta = ps.parse_frontmatter(path)
        desc = meta.get("description", "")
        check("description niet leeg", bool(desc))
        check("beschrijving bevat tekst", "beschrijving" in desc)
    finally:
        path.unlink()


def test_missing_frontmatter() -> None:
    """Test fout bij ontbrekende frontmatter."""
    print("\n[5] Fout bij ontbrekende frontmatter")
    content = """# Geen frontmatter hier

Content zonder ---
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        f.flush()
        path = Path(f.name)

    try:
        try:
            meta = ps.parse_frontmatter(path)
            check("fout gegooid", False, "geen ValidationError")
        except ps.ValidationError as e:
            check("ValidationError gegooid", "geen frontmatter" in str(e))
    finally:
        path.unlink()


def test_unclosed_frontmatter() -> None:
    """Test gedrag bij niet-gesloten frontmatter.

    NB: De huidige parser splitst op '---' en accepteert content
    zonder tweede '---'. Dit is beperkt YAML-parsing.
    """
    print("\n[6] Gedrag bij niet-gesloten frontmatter")
    content = """---
name: unclosed
description: Test
version: 1.0.0
last_updated: 2026-01-01
author: Test
license: MIT
jurisdiction: NL
compatibility: [ClaudeCode]
source: docs/workflow.md

Content zonder afsluitende ---
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        f.flush()
        path = Path(f.name)

    try:
        meta = ps.parse_frontmatter(path)
        # Parser vindt eerste '---', splitst, neemt block 0 (leeg) en 1 (content)
        # Dit is beperkte YAML-parsing - de test documenteert huidig gedrag
        check("parser accepteert (beperkt gedrag)", isinstance(meta, dict))
    finally:
        path.unlink()


def test_quoted_values() -> None:
    """Test quoted values in frontmatter.

    NB: De huidige parser verwijdert GEEN quotes rond waarden.
    Quotes worden beschouwd als onderdeel van de waarde.
    """
    print("\n[7] Quoted string values (huidig gedrag)")
    content = """---
name: quoted-test
description: Test met quoted waarden in de beschrijving.
version: 1.0.0
last_updated: 2026-01-01
author: "Test Author"
license: "CC-BY-4.0"
jurisdiction: NL
compatibility: [ClaudeCode]
source: docs/workflow.md
---
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        f.flush()
        path = Path(f.name)

    try:
        meta = ps.parse_frontmatter(path)
        # Huidig gedrag: quotes blijven staan
        check("author MET quotes (huidig gedrag)", meta.get("author") == '"Test Author"')
        check("license MET quotes (huidig gedrag)", meta.get("license") == '"CC-BY-4.0"')
    finally:
        path.unlink()


def test_empty_lines_in_frontmatter() -> None:
    """Test dat lege regels in frontmatter worden overgeslagen."""
    print("\n[8] Lege regels worden overgeslagen")
    content = """---

name: empty-line-test

description: Test.

version: 1.0.0

last_updated: 2026-01-01

author: Test

license: MIT

jurisdiction: NL

compatibility: [ClaudeCode]

source: docs/workflow.md

---
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        f.flush()
        path = Path(f.name)

    try:
        meta = ps.parse_frontmatter(path)
        check("name geparseerd ondanks lege regels", meta.get("name") == "empty-line-test")
        check("description geparseerd", meta.get("description") == "Test.")
    finally:
        path.unlink()


def test_indented_values() -> None:
    """Test dat geïndenteerde waarden worden toegevoegd aan current key."""
    print("\n[9] Geïndenteerde waarden worden toegevoegd aan current key")
    content = """---
name: indented-test
description: >
  Dit is een beschrijving
  die over meerdere regels
  wordt voortgezet.
version: 1.0.0
last_updated: 2026-01-01
author: Test
license: MIT
jurisdiction: NL
compatibility: [ClaudeCode]
source: docs/workflow.md
---
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        f.flush()
        path = Path(f.name)

    try:
        meta = ps.parse_frontmatter(path)
        desc = meta.get("description", "")
        check("beschrijving bevat alle regels", "beschrijving" in desc and "wordt" in desc)
    finally:
        path.unlink()


def main() -> int:
    print("=" * 70)
    print("Unit tests: parse_frontmatter()")
    print("=" * 70)

    test_minimal_frontmatter()
    test_inline_list()
    test_inline_map()
    test_multiline_description()
    test_missing_frontmatter()
    test_unclosed_frontmatter()
    test_quoted_values()
    test_empty_lines_in_frontmatter()
    test_indented_values()

    print("\n" + "=" * 70)
    print(f"Resultaat: {PASS} PASS / {FAIL} FAIL")
    print("=" * 70)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
