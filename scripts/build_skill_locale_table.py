#!/usr/bin/env python3
"""Build local EN↔RU locale table from official wiki data (scripts/wiki_ru_official.json)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI_JSON = Path(__file__).resolve().parent / "wiki_ru_official.json"


def load_data_skills() -> dict[str, dict]:
    js = (ROOT / "hero-builder-data.js").read_text(encoding="utf-8")
    block = re.search(r"skills:\s*\{(.*?)\n\s*\},\s*\n\s*classes:", js, re.S)
    if not block:
        return {}
    entries = re.findall(
        r'(?:"([^"]+)"|([A-Za-z][\w\' ]*?)):\s*\{[^}]*adv:\s*\[(.*?)\],\s*exp:\s*\[(.*?)\]',
        block.group(1),
        re.S,
    )
    out = {}
    for quoted, bare, adv, exp in entries:
        name = quoted or bare.strip()
        out[name] = {
            "adv": re.findall(r'"([^"]+)"', adv),
            "exp": re.findall(r'"([^"]+)"', exp),
        }
    return out


def load_data_subclasses() -> list[str]:
    js = (ROOT / "hero-builder-data.js").read_text(encoding="utf-8")
    subs: set[str] = set()
    for m in re.finditer(r"subclasses:\s*\{", js):
        chunk = js[m.end():]
        depth = 1
        i = 0
        while i < len(chunk) and depth > 0:
            if chunk[i] == "{":
                depth += 1
            elif chunk[i] == "}":
                depth -= 1
            i += 1
        block = chunk[: i - 1]
        for sm in re.finditer(r'(?:"([^"]+)"|(\w+)):\s*\{', block):
            name = sm.group(1) or sm.group(2)
            if name not in ("bonus", "bonusEn", "bonusRu", "skills"):
                subs.add(name)
    return sorted(subs)


def load_project_locale() -> dict:
    disp = (ROOT / "hero-builder-display-locale.js").read_text(encoding="utf-8")

    def extract_ru(key: str) -> dict[str, str]:
        m = re.search(rf"{key}:\s*\{{", disp)
        if not m:
            return {}
        start = disp.find("ru:", m.start())
        if start < 0:
            return {}
        brace = disp.find("{", start + 3)
        depth = 0
        i = brace
        while i < len(disp):
            if disp[i] == "{":
                depth += 1
            elif disp[i] == "}":
                depth -= 1
                if depth == 0:
                    body = disp[brace + 1 : i]
                    return dict(re.findall(r'"([^"]+)":\s*"((?:\\.|[^"\\])*)"', body))
            i += 1
        return {}

    return {
        "skills": extract_ru("skills"),
        "subskills": extract_ru("subskills"),
        "subclasses": extract_ru("subclasses"),
    }


def compare_status(wiki: str | None, project: str | None) -> str:
    if not wiki:
        return "MISSING WIKI"
    if not project:
        return "MISSING PROJECT"
    if wiki.strip() == project.strip():
        return "OK"
    return "MISMATCH"


def main() -> int:
    if not WIKI_JSON.is_file():
        print(f"ERROR: {WIKI_JSON} not found")
        return 1

    wiki = json.loads(WIKI_JSON.read_text(encoding="utf-8"))
    data_skills = load_data_skills()
    subclass_keys = load_data_subclasses()
    project = load_project_locale()

    rows: list[dict] = []
    wiki_ru = {"skills": dict(wiki.get("skills", {})), "subskills": dict(wiki.get("subskills", {})), "subclasses": dict(wiki.get("subclasses", {}))}

    for key in sorted(data_skills.keys(), key=lambda x: x.lower()):
        ru_skill = wiki_ru["skills"].get(key)
        proj_skill = project["skills"].get(key)
        rows.append({
            "type": "skill",
            "en_key": key,
            "ru_wiki": ru_skill or "",
            "ru_project": proj_skill or "",
            "status": compare_status(ru_skill, proj_skill),
        })
        for sub_en in data_skills[key]["adv"] + data_skills[key]["exp"]:
            ru_sub = wiki_ru["subskills"].get(sub_en)
            proj_sub = project["subskills"].get(sub_en)
            rows.append({
                "type": "subskill",
                "en_key": sub_en,
                "parent": key,
                "ru_wiki": ru_sub or "",
                "ru_project": proj_sub or "",
                "status": compare_status(ru_sub, proj_sub),
            })

    for en in subclass_keys:
        ru_w = wiki_ru["subclasses"].get(en) or project["subclasses"].get(en)
        proj = project["subclasses"].get(en)
        st = compare_status(wiki_ru["subclasses"].get(en), proj) if wiki_ru["subclasses"].get(en) else "MISSING WIKI"
        if wiki_ru["subclasses"].get(en) and proj and wiki_ru["subclasses"][en] == proj:
            st = "OK"
        elif not wiki_ru["subclasses"].get(en):
            st = "MISSING WIKI"
        rows.append({
            "type": "subclass",
            "en_key": en,
            "ru_wiki": wiki_ru["subclasses"].get(en, ""),
            "ru_project": proj or "",
            "status": st,
        })

    stats: dict[str, int] = {}
    for r in rows:
        stats[r["status"]] = stats.get(r["status"], 0) + 1

    json_path = ROOT / "_skill_locale_ru.json"
    json_path.write_text(json.dumps(wiki_ru, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Таблица соответствия EN ↔ RU (официальная wiki)",
        "",
        "Источник: `scripts/wiki_ru_official.json` (кэш страниц `/ru`).",
        "",
        "## Сводка",
        "",
    ]
    for k, v in sorted(stats.items()):
        lines.append(f"- **{k}**: {v}")
    lines.append("")

    def section(title: str, types: set[str], only_status: str | None = None):
        lines.append(f"## {title}")
        lines.append("")
        lines.append("| type | en_key | ru_wiki | ru_project | status |")
        lines.append("|------|--------|---------|------------|--------|")
        for r in rows:
            if r["type"] not in types:
                continue
            if only_status and r["status"] != only_status:
                continue
            flag = " ⚠" if r["status"] == "MISSING WIKI" else (" ↔" if r["status"] == "MISMATCH" else "")
            lines.append(f"| {r['type']} | {r['en_key']} | {r['ru_wiki']} | {r['ru_project']} | **{r['status']}**{flag} |")
        lines.append("")

    section("Навыки", {"skill"})
    section("Расхождения — навыки и поднавыки", {"skill", "subskill"}, "MISMATCH")
    section("⚠ Недостаёт в wiki", {"skill", "subskill", "subclass"}, "MISSING WIKI")
    section("Подклассы", {"subclass"})

    md_path = ROOT / "_skill_locale_table.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {md_path.name}, {json_path.name}")
    print("Stats:", stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
