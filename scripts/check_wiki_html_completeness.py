#!/usr/bin/env python3
"""Read-only completeness check for rared html wiki exports."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_DIR = ROOT / "rared html"

EXPECTED_SKILLS = [
    "Offense", "Defense", "Leadership", "Luck", "Resistance", "Tactics", "Battlecraft",
    "Siegecraft", "Recruitment", "Combat",
    "Battle Magic", "Sorcery", "Summon Avatar", "Wisdom", "Daylight Magic", "Nightshade Magic",
    "Arcane Magic", "Primal Magic", "Thaumaturgy",
    "Diplomacy", "Logistics", "Scouting", "Insight", "Economy",
    "Righteousness", "Necromancy", "Abyssal Communion", "Triumvirate's Strength", "Murmuring", "Summon Swarm",
]


def norm(name: str) -> str:
    return name.replace("Defence", "Defense").replace("Offence", "Offense").strip()


def norm_sub(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def skill_from_filename(path: Path) -> str | None:
    name = path.stem.split(" - ")[0]
    if name in ("Skills", "Hero Skill Synergies"):
        return None
    if name.startswith("Summon Avatar"):
        return "Summon Avatar"
    return name


def parse_tiers(html: str) -> tuple[bool, bool, bool]:
    has_basic = bool(re.search(r"Basic&nbsp;", html) or re.search(r"<b>Basic\s", html))
    has_adv = bool(re.search(r"Advanced&nbsp;", html) or re.search(r"<b>Advanced\s", html))
    has_exp = bool(re.search(r"Expert&nbsp;", html) or re.search(r"<b>Expert\s", html))
    return has_basic, has_adv, has_exp


def extract_b(section: str | None) -> list[str]:
    if not section:
        return []
    out = []
    for m in re.finditer(r"<b>([^<]+)</b>", section):
        n = m.group(1).strip()
        if re.match(r"^(Basic|Advanced|Expert)\s", n):
            continue
        out.append(n)
    return out


def parse_skill_page(html: str) -> dict:
    tiers = parse_tiers(html)
    adv_match = re.search(r"Advanced&nbsp;[^<]+</b>.*?(?=Expert&nbsp;)", html, re.S)
    exp_match = re.search(
        r"Expert&nbsp;[^<]+</b>.*?(?=<h3|<h2|Skill Synergies|Artifact Effects)",
        html,
        re.S,
    )
    adv = extract_b(adv_match.group(0) if adv_match else "")
    exp = extract_b(exp_match.group(0) if exp_match else "")
    return {"tiers": tiers, "adv": adv, "exp": exp}


def load_js_skills() -> dict[str, dict]:
    js = (ROOT / "hero-builder-data.js").read_text(encoding="utf-8")
    skill_block = re.search(r"skills:\s*\{(.*?)\n\s*\},\s*\n\s*classes:", js, re.S)
    if not skill_block:
        return {}
    # Keys may be quoted ("Battle Magic") or bare (Offense, Defence)
    entries = re.findall(
        r'(?:"([^"]+)"|([A-Za-z][\w\' ]*?)):\s*\{[^}]*adv:\s*\[(.*?)\],\s*exp:\s*\[(.*?)\]',
        skill_block.group(1),
        re.S,
    )
    result = {}
    for quoted, bare, adv, exp in entries:
        name = quoted or bare.strip()
        result[norm(name)] = {
            "adv": re.findall(r'"([^"]+)"', adv),
            "exp": re.findall(r'"([^"]+)"', exp),
        }
    return result


def js_skill_lookup(js_skills: dict[str, dict], wiki_skill: str) -> dict | None:
    """Find JS skill entry; wiki uses Defense, JS may use Defence."""
    key = norm(wiki_skill)
    if key in js_skills:
        return js_skills[key]
    for js_key, data in js_skills.items():
        if norm(js_key) == key:
            return data
    return None


def main() -> int:
    html_files = sorted(HTML_DIR.glob("*.html"))
    if not HTML_DIR.is_dir():
        print(f"ERROR: folder not found: {HTML_DIR}")
        return 1

    parsed: dict[str, dict] = {}
    for f in html_files:
        skill = skill_from_filename(f)
        if not skill:
            continue
        html = f.read_text(encoding="utf-8", errors="replace")
        data = parse_skill_page(html)
        data["file"] = f.name
        parsed[skill] = data

    missing_pages = [s for s in EXPECTED_SKILLS if not any(norm(k) == norm(s) for k in parsed)]

    print("=== WIKI HTML COMPLETENESS CHECK ===")
    print(f"Folder: {HTML_DIR}")
    print(f"HTML files: {len(html_files)} (skill pages: {len(parsed)})")
    print()

    print("--- Missing skill pages ---")
    if missing_pages:
        for m in missing_pages:
            print(f"  MISSING: {m}")
    else:
        print("  None (30/30)")

    print()
    print("--- Incomplete skill data ---")
    incomplete = []
    for skill in EXPECTED_SKILLS:
        key = next((k for k in parsed if norm(k) == norm(skill)), None)
        if not key:
            continue
        d = parsed[key]
        probs = []
        if not all(d["tiers"]):
            probs.append(f"missing tier rows: basic={d['tiers'][0]} adv={d['tiers'][1]} exp={d['tiers'][2]}")
        if len(d["adv"]) != 3:
            probs.append(f"advanced subskills={len(d['adv'])} (expected 3): {d['adv']}")
        if len(d["exp"]) != 3:
            probs.append(f"expert subskills={len(d['exp'])} (expected 3): {d['exp']}")
        if probs:
            incomplete.append((skill, probs))
            print(f"  {skill}: {'; '.join(probs)}")

    if not incomplete:
        print("  None — all skills have Basic/Advanced/Expert and 3+3 subskills")

    print()
    print("--- hero-builder-data.js vs wiki ---")
    js_skills = load_js_skills()
    data_mismatches = []
    for skill in EXPECTED_SKILLS:
        key = next((k for k in parsed if norm(k) == norm(skill)), None)
        if not key:
            continue
        d = parsed[key]
        js = js_skill_lookup(js_skills, skill)
        if not js:
            data_mismatches.append((skill, "missing in hero-builder-data.js"))
            continue
        adv_html = {norm_sub(x) for x in d["adv"]}
        exp_html = {norm_sub(x) for x in d["exp"]}
        adv_js = {norm_sub(x) for x in js["adv"]}
        exp_js = {norm_sub(x) for x in js["exp"]}
        if adv_html != adv_js:
            data_mismatches.append((skill, f"adv wiki={d['adv']} js={js['adv']}"))
        if exp_html != exp_js:
            data_mismatches.append((skill, f"exp wiki={d['exp']} js={js['exp']}"))

    if data_mismatches:
        for s, m in data_mismatches:
            print(f"  MISMATCH {s}: {m}")
    else:
        print("  All subskills match hero-builder-data.js")

    print()
    print("--- Meta pages ---")
    meta = [f.name for f in html_files if skill_from_filename(f) is None]
    for m in meta:
        print(f"  {m}")

    print()
    print("=== RESULT ===")
    failed = bool(missing_pages or incomplete)
    if failed:
        print("FAIL — missing or incomplete skill data in rared html")
        return 1
    print("PASS — all 30 skills present and structurally complete in rared html")
    if data_mismatches:
        print(f"NOTE — {len(data_mismatches)} mismatches vs hero-builder-data.js (app data may need sync)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
