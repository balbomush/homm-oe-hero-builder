#!/usr/bin/env python3
"""Generate specialty_ru_overrides.json from specialty_en_overrides.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

GROWTH_FULL_RE = re.compile(
    r"^(?P<unit>.+?) growth in your cities increases by 1\. Under (?:her|his) command, (?P<cmd>.+?) gain 1 Speed, 1 Initiative, and 20% HP\. "
    r"Their Attack and Defen[cs]e increase by 1 for every 3 hero levels, and enemy (?P<enemy>.+?) lose an equal amount of Attack and Defen[cs]e\.$",
    re.I,
)
GROWTH_SHORT_RE = re.compile(
    r"^(?P<unit>.+?) growth in your cities increases by 1\. Under (?:her|his) command, (?P<cmd>.+?) gain 1 Speed, 1 Initiative, and 20% HP\. "
    r"Their Attack and Defen[cs]e increase by 1 for every 3 hero levels\.$",
    re.I,
)
MAGIC_SCHOOL_RE = re.compile(
    r"^(?P<school>.+ Magic) spells cast by the hero are treated as \+1 level higher\.$",
    re.I,
)
RESOURCE_RE = re.compile(
    r"^Produces \+1 (?P<res>Gem|Gems|Crystals?) per day, plus another \+1 for every 5 hero levels\. "
    r"Increases the amount of (?P<res_map>Gems|Crystals?) found on the map by 100%\.$",
    re.I,
)
MASTERFUL_CAST_RE = re.compile(
    r"^(?:She|He) starts with the Masterful (?P<spell>.+?) spell\. (?P<detail>.+?) "
    r"While casting this spell, effective Spell Power is increased by 1 for every (?P<lv>.+?)\.$",
    re.I,
)
MASTERFUL_CAST_ALT_RE = re.compile(
    r"^Starts with the Masterful (?P<spell>.+?) spell\. (?P<detail>.+?) "
    r"While casting, effective Spell Power increases by 1 for every (?P<lv>.+?)\.$",
    re.I,
)


def tr_growth(m: re.Match, with_enemy: bool) -> str:
    unit, cmd, enemy = m.group("unit"), m.group("cmd"), m.group("enemy") if with_enemy else None
    base = (
        f"Рост {unit} в городах +1/нед. Под командованием героя {cmd} получают +1 к скорости, +1 к инициативе и +20% HP. "
        f"Их атака и защита +1 за каждые 3 ур. героя"
    )
    if with_enemy:
        base += f"; у вражеских {enemy} атака и защита снижаются на столько же"
    return base + "."


def translate_specialty(text: str) -> str:
    text = text.strip()
    exact = {
        "Has +10% Movement points, plus 2.5% more for every 6 hero levels. Moves significantly more efficiently on roads.": (
            "Имеет +10% очков передвижения и ещё +2.5% за каждые 6 ур. героя. Значительно эффективнее двигается по дорогам."
        ),
        "Has +10% Movement points, plus 2.5% more for every 6 hero levels.": (
            "Имеет +10% очков передвижения и ещё +2.5% за каждые 6 ур. героя."
        ),
        "The hero gains +1 sight radius, plus another +1 for every 5 hero levels.": (
            "Герой получает +1 к радиусу обзора и ещё +1 за каждые 5 ур. героя."
        ),
        "All friendly creatures gain +1 Morale. The chance of an additional turn increases by 2% per Morale point, plus 1% more for every 4 hero levels.": (
            "Все союзники получают +1 к морали. Шанс дополнительного хода +2% за пункт морали и ещё +1% за каждые 4 ур. героя."
        ),
        "All friendly creatures gain +1 Morale. The chance of an additional turn increases by 2% per Morale point.": (
            "Все союзники получают +1 к морали. Шанс дополнительного хода +2% за пункт морали."
        ),
        "Friendly creatures gain 20% of his Attack and Defense (as Attack and Defense), plus another 5% for every 6 hero levels.": (
            "Союзники получают 20% атаки и защиты героя (как атаку и защиту) и ещё +5% за каждые 6 ур. героя."
        ),
        "Heroic Strike deals +10 base Damage, plus another +5 for every 6 hero levels.": (
            "Героический удар наносит +10 базового урона и ещё +5 за каждые 6 ур. героя."
        ),
        "The hero gains +1 spell cap for each Global Map spell. Maximum mana increases by 10%, plus another 5% for every 5 hero levels.": (
            "+1 слот глобального заклинания за каждое изученное глобальное заклинание. Максимальная мана +10% и ещё +5% за каждые 5 ур. героя."
        ),
        "When leveling up, gains 1 additional attribute point(s) for every 2 hero levels. Gains +5% XP for every 2 hero levels.": (
            "При повышении уровня получает +1 к случайной характеристике за каждые 2 ур. героя. +5% опыта за каждые 2 ур. героя."
        ),
        "Produces +500 gold per day, plus another +250 for every 5 hero levels.": (
            "+500 золота/день и ещё +250 за каждые 5 ур. героя."
        ),
        "Friendly creatures' Defense increases by 10% of the hero's Defense, plus 2% more for every 4 hero levels.": (
            "Защита союзников увеличивается на 10% от защиты героя и ещё +2% за каждые 4 ур. героя."
        ),
        "Persuasion Power increases by 10%, plus 2% more for every 4 hero levels.": (
            "Сила убеждения +10% и ещё +2% за каждые 4 ур. героя."
        ),
        "Friendly creatures' Attack increases by 10% of the hero's Attack, plus 2% more for every 4 hero levels.": (
            "Атака союзников увеличивается на 10% от атаки героя и ещё +2% за каждые 4 ур. героя."
        ),
        "Magic Damage taken by friendly creatures is reduced by 10%, plus 2% more for every 4 hero levels.": (
            "Получаемый союзниками магический урон снижен на 10% и ещё на 2% за каждые 4 ур. героя."
        ),
        "Magic Damage dealt increases by 10%, plus 2% more for every 4 hero levels.": (
            "Наносимый магический урон +10% и ещё +2% за каждые 4 ур. героя."
        ),
        "Maximum mana increases by 10%, plus 5% more for every 5 hero levels.": (
            "Максимальная мана +10% и ещё +5% за каждые 5 ур. героя."
        ),
        "The hero and army gain +1 Luck, plus +1 more for every 6 hero levels.": (
            "Герой и армия получают +1 к удаче и ещё +1 за каждые 6 ур. героя."
        ),
        "The hero gains +20% XP, plus 5% more for every 4 hero levels.": (
            "Герой получает +20% опыта и ещё +5% за каждые 4 ур. героя."
        ),
        "The hero can use the Spellbook one additional time per battle round.": (
            "Герой может использовать книгу заклинаний один дополнительный раз за боевой раунд."
        ),
        "Friendly creatures' Attack and Defense increase based on the hero's Spell Power and Knowledge.": (
            "Атака и защита союзников растут от силы заклинаний и знания героя."
        ),
        "Tier 6 creatures in the army gain +1 Speed, +1 Initiative, +20% HP. Their Attack and Defence increase by 1 for every 3 hero levels.": (
            "Существа T6 в армии получают +1 к скорости, +1 к инициативе и +20% HP. Их атака и защита +1 за каждые 3 ур. героя."
        ),
        "Universal Necromancer hero. Starts with Advanced Necromancy.": (
            "Универсальный некромант. Начинает с продвинутой некромантии."
        ),
        "Universal Schism hero. Starts with Advanced Abyssal Communion.": (
            "Универсальный герой Раскола. Начинает с продвинутого бездонного общения."
        ),
        "When friendly creatures wait or skip, they gain additional Attack or Defense bonuses.": (
            "Когда союзники ждут или пропускают ход, они получают дополнительные бонусы к атаке или защите."
        ),
        "Movement takes no terrain penalties. The hero gains +1 sight radius, plus another +1 for every 5 hero levels.": (
            "Движение без штрафов местности. +1 к радиусу обзора и ещё +1 за каждые 5 ур. героя."
        ),
        "Creatures in his army deal +10% basic attack Damage, plus an additional 1% for every 2 hero levels. Additionally, they deal +1% Ranged and Long Reach Damage for every 2 hero levels.": (
            "Существа армии наносят +10% урона базовых атак и +1% за каждые 2 ур. героя. Дополнительно +1% урона дальнего/длинного радиуса за каждые 2 ур. героя."
        ),
        "Creatures in her army deal +10% basic attack Damage, plus an additional 1% for every 2 hero levels. Additionally, they deal +1% Ranged and Long Reach Damage for every 2 hero levels.": (
            "Существа армии наносят +10% урона базовых атак и +1% за каждые 2 ур. героя. Дополнительно +1% урона дальнего/длинного радиуса за каждые 2 ур. героя."
        ),
        "She has +1 Luck, and creatures under her command have an increased chance of triggering a Lucky Strike: +2% chance per Luck point. For every 4 levels, this bonus increases by 1%.": (
            "+1 к удаче. Союзники получают +2% шанса удачного удара за пункт удачи; бонус +1% за каждые 4 ур. героя."
        ),
        "She produces +1 Crystals per day, plus another +1 for every 5 hero levels. Increases the amount of Crystals found on the map by 100%.": (
            "+1 кристалл/день и ещё +1 за каждые 5 ур. героя. Количество кристаллов на карте увеличено на 100%."
        ),
        "Keeps the army when fleeing from battle against neutral squads. +5% Persuasion Power when using Diplomacy, plus another 1% for every 4 hero levels.": (
            "Сохраняет армию при бегстве от нейтральных отрядов. +5% силы убеждения при дипломатии и ещё +1% за каждые 4 ур. героя."
        ),
        "She gains +1 spell cap for each Global Map spell. Her maximum mana increases by 10%, plus another 5% for every 5 hero levels.": (
            "+1 слот глобального заклинания за каждое глобальное заклинание. Максимальная мана +10% и ещё +5% за каждые 5 ур. героя."
        ),
        "Her summoned Avatar is immune to Magic Damage. When casting Summon Avatar, its effective Spell Power is increased by +1 per 3 hero levels.": (
            "Призванный аватар невосприимчив к магическому урону. При касте Summon Avatar эффективная сила заклинаний +1 за каждые 3 ур. героя."
        ),
        "At the beginning of each round, he generates +2 Focus Point(s), plus another +1 for every 3 hero levels. The enemy loses the same amount of Focus Points.": (
            "В начале каждого раунда генерирует +2 фокуса и ещё +1 за каждые 3 ур. героя. Враг теряет столько же фокуса."
        ),
        "Starts with only Waurms. Unique army composition specialist.": (
            "Начинает только с Waurms. Уникальная специализация на состав армии."
        ),
        "Creatures deal increased damage when Morale triggers.": (
            "Существа наносят повышенный урон при срабатывании морали."
        ),
        "Starts with Advanced Summon Swarm and improved Fire Larvae synergy.": (
            "Начинает с продвинутого Summon Swarm и улучшенной синергией Fire Larvae."
        ),
        "Friendly creatures gain improved Initiative when using Tactics.": (
            "Союзники получают улучшенную инициативу от бонусов тактики."
        ),
        "Haste and initiative bonuses for friendly creatures.": (
            "Бонусы ускорения и инициативы для союзников."
        ),
        "Produces +1 Crystal per day, plus another +1 for every 5 hero levels.": (
            "+1 кристалл/день и ещё +1 за каждые 5 ур. героя."
        ),
        "Summon Avatar and blink-style mobility bonuses.": (
            "Усиленный Summon Avatar и бонусы мобильности в стиле blink."
        ),
        "Primal Magic lock and control specialist.": (
            "Специалист по блокировке и контролю Primal Magic."
        ),
        "Friendly creatures' Defense increases significantly based on hero Defense.": (
            "Защита союзников значительно растёт от защиты героя."
        ),
        "Deals +10% Damage with spells, plus 1% more for every 2 hero levels. Damage from enemy hero spells is reduced by the same value.": (
            "Наносит +10% урона заклинаниями и +1% за каждые 2 ур. героя. Урон вражеских заклинаний героя снижается на то же значение."
        ),
        "Friendly creatures gain improved Initiative from Tactics bonuses.": (
            "Союзники получают улучшенную инициативу от бонусов тактики."
        ),
        "Healing Water restores additional HP based on hero level and heals more stacks.": (
            "Healing Water восстанавливает дополнительное HP в зависимости от уровня героя и лечит больше отрядов."
        ),
        "Blessing grants additional Attack and Defense scaling with hero level.": (
            "Blessing даёт дополнительные атаку и защиту, растущие с уровнем героя."
        ),
        "Vulnerability reduces enemy Defense more effectively and scales with hero level.": (
            "Vulnerability эффективнее снижает защиту врагов и масштабируется с уровнем героя."
        ),
    }
    if text in exact:
        return exact[text]

    m = GROWTH_FULL_RE.match(text)
    if m:
        return tr_growth(m, True)
    m = GROWTH_SHORT_RE.match(text)
    if m:
        return tr_growth(m, False)

    m = RESOURCE_RE.match(text)
    if m:
        if "Crystal" in m.group("res"):
            return "+1 кристалл/день и ещё +1 за каждые 5 ур. героя. Количество кристаллов на карте увеличено на 100%."
        return "+1 самоцвет/день и ещё +1 за каждые 5 ур. героя. Количество самоцветов на карте увеличено на 100%."

    m = MAGIC_SCHOOL_RE.match(text)
    if m:
        school = m.group("school")
        schools_ru = {
            "Arcane Magic": "тайной магии",
            "Nightshade Magic": "магии сумрака",
            "Daylight Magic": "магии дневного света",
            "Primal Magic": "первичной магии",
        }
        return f"Заклинания {schools_ru.get(school, school)}, которыми кастует герой, считаются на +1 уровень выше."

    if " is improved and scales with hero level" in text:
        name = text.split(" is improved")[0]
        return f"{name} усилен и масштабируется с уровнем героя."

    masterful_details = {
        "Early Start": ("Early Start", "версия не снимается"),
        "Fireball": ("Fireball", "увеличенная область поражения"),
        "Guillotine": ("Guillotine", "урон растёт вдвое быстрее при повторном касте на одну цель"),
        "Firewall": ("Firewall", "версия действует на +1 раунд дольше"),
        "Ice Bolt": ("Ice Bolt", "штраф к инициативе этой версии вдвое сильнее"),
        "Cave In": ("Cave In", "препятствия нужно повредить на +1 раз больше для уничтожения"),
        "Mirror Copy": ("Mirror Copy", "версия может нацеливаться на вражеских существ"),
        "Chain Lightning": ("Chain Lightning", "версия теряет вдвое меньше урона при прыжках между целями"),
    }
    for pattern_re in (MASTERFUL_CAST_RE, MASTERFUL_CAST_ALT_RE):
        m = pattern_re.match(text)
        if m:
            spell = m.group("spell")
            lv = m.group("lv").replace("hero level(s)", "ур. героя").replace("3 hero levels", "3 ур. героя")
            detail = m.group("detail")
            if spell in masterful_details:
                _, ru_detail = masterful_details[spell]
            elif "cannot be dispelled" in detail:
                ru_detail = "версия не снимается"
            elif "larger area" in detail:
                ru_detail = "увеличенная область поражения"
            elif "twice as fast" in detail:
                ru_detail = "урон растёт вдвое быстрее при повторном касте на одну цель"
            elif "stays active" in detail:
                ru_detail = "версия действует на +1 раунд дольше"
            elif "Initiative penalty" in detail:
                ru_detail = "штраф к инициативе этой версии вдвое сильнее"
            elif "obstacles" in detail:
                ru_detail = "препятствия нужно повредить на +1 раз больше для уничтожения"
            elif "target enemy" in detail:
                ru_detail = "версия может нацеливаться на вражеских существ"
            elif "half as much Damage" in detail:
                ru_detail = "версия теряет вдвое меньше урона при прыжках между целями"
            else:
                ru_detail = detail
            return (
                f"Начинает с Masterful {spell} — {ru_detail}. "
                f"При касте эффективная сила заклинаний +1 за каждые {lv}."
            )

    raise ValueError(f"No translation: {text[:100]}...")


def main() -> None:
    en = json.loads((ROOT / "specialty_en_overrides.json").read_text(encoding="utf-8"))
    ru = {}
    errors = []
    for hid, desc in en.items():
        try:
            ru[hid] = translate_specialty(desc)
        except ValueError as e:
            errors.append((hid, str(e)))
    if errors:
        for hid, err in errors:
            print(f"FAIL {hid}: {err}")
        raise SystemExit(1)
    out_path = ROOT / "specialty_ru_overrides.json"
    out_path.write_text(json.dumps(ru, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(ru)} entries to {out_path.name}")


if __name__ == "__main__":
    main()
