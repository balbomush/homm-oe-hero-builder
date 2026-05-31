#!/usr/bin/env python3
"""Export synergies.json and hero-builder-synergies.js for HoMM OE hero configurator."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SKILL_ALIAS = {
    "Offence": "Offense",
    "Intelligence": "Wisdom",
    "Ascension": "Righteousness",
    "Call Swarm": "Summon Swarm",
}

FACTION_SKILL = {
    "Temple": "Righteousness",
    "Necropolis": "Necromancy",
    "Grove": "Murmuring",
    "Dungeon": "Triumvirate's Strength",
    "Hive": "Summon Swarm",
    "Schism": "Abyssal Communion",
}

UNIVERSAL_IDS = {"lord-edgar", "tarius", "funerella", "mara-matha", "dh-vri"}

HERO_SUBCLASS_HINTS = {
    "kestrel": "Swashbuckler",
    "aeos-the-exalted": "Swashbuckler",
    "keandra": "Paragon",
    "pip": "Grand Inquisitor",
    "julius": "Ascendant",
    "clarissa": "Ascendant",
    "bulwark": "Walking Rot",
    "king-of-kings": "Walking Rot",
    "kelghul": "Walking Rot",
    "artorius-veritas": "Walking Rot",
    "natalida": "Harbinger of Doom",
    "mag": "Soulweaver",
    "adhan": "Soulweaver",
    "milossa-the-golden": "Chronomancer",
    "devir-son-of-devir": "Balthazar's Bodyguard",
    "rhea": "Silvertongue's Envoy",
    "mouaren": "Silvertongue's Envoy",
    "glastor": "Great Merchant",
    "blackhorn": "Unbound",
    "iron-master": "Unfeeling",
    "j-nhei": "Unfeeling",
    "martyr-tho": "Unbound",
    "the-eye-collective": "Unfathomable",
    "t-lketh": "Unfathomable",
    "radavok": "Unfathomable",
}

NAME_RU = {
    "Jänhei": "Янхей",
    "Tōlketh": "Толкет",
    "Ra'Davok": "Ра'Давок",
    "Dhüvri": "Дhüvri",
    "Kel'Ghul": "Кел'Гул",
    "Hel'Ghat": "Хел'Гат",
    "Martyr Tho": "Мученик То",
}

RU_TERMS = [
    (r"\bMovement points\b", "очков передвижения"),
    (r"\bhero levels?\b", "ур. героя"),
    (r"\bhero level\b", "уровень героя"),
    (r"\bfriendly creatures?\b", "дружественные существа"),
    (r"\benemy creatures?\b", "вражеские существа"),
    (r"\bFriendly creatures\b", "Дружественные существа"),
    (r"\bPersuasion Power\b", "силу убеждения"),
    (r"\bsight radius\b", "радиус обзора"),
    (r"\bMagic Damage\b", "магический урон"),
    (r"\bSpell Power\b", "силу заклинаний"),
    (r"\bHeroic Strike\b", "Героический удар"),
    (r"\bFocus Point\(s\)\b", "очков Focus"),
    (r"\bFocus Points\b", "очков Focus"),
    (r"\bLucky Strike\b", "Lucky Strike"),
    (r"\bMorale\b", "Morale"),
    (r"\bLuck\b", "Luck"),
    (r"\bAttack and Defence\b", "Attack и Defence"),
    (r"\bAttack and Defense\b", "Attack и Defense"),
    (r"\bgrowth in your cities increases by 1\b", "рост в городах +1/нед."),
    (r"\bStarts with\b", "Начинает с"),
    (r"\bUniversal\b", "Универсальный"),
    (r"\bAdvanced\b", "Продвинутый"),
    (r"\bNecromancy\b", "Necromancy"),
    (r"\bAbyssal Communion\b", "Abyssal Communion"),
    (r"\bMaximum mana\b", "максимальная мана"),
    (r"\bXP\b", "опыт"),
    (r"\bGem\b", "самоцвет"),
    (r"\bGems\b", "самоцветы"),
    (r"\bCrystals\b", "кристаллы"),
    (r"\bgold per day\b", "золота/день"),
    (r"\bRanged and Long Reach Damage\b", "урон Ranged и Long Reach"),
    (r"\bbasic attack Damage\b", "урон базовых атак"),
    (r"\bWhen leveling up\b", "При повышении уровня"),
    (r"\badditional attribute point\(s\)\b", "доп. очко характеристик"),
    (r"\bGlobal Map spell\b", "глобальное заклинание карты"),
    (r"\bSpellbook\b", "книгу заклинаний"),
    (r"\bbattle round\b", "боевой раунд"),
    (r"\bterrain penalties\b", "штрафы местности"),
    (r"\bwait or skip\b", "Wait/Skip"),
    (r"\bSummon Avatar\b", "Summon Avatar"),
    (r"\bDaylight Magic\b", "Daylight Magic"),
    (r"\bNightshade Magic\b", "Nightshade Magic"),
    (r"\bArcane Magic\b", "Arcane Magic"),
    (r"\bPrimal Magic\b", "Primal Magic"),
    (r"\bMasterful\b", "Masterful"),
    (r"\beffective Spell Power\b", "эффективная сила заклинаний"),
    (r"\bInitiative\b", "Initiative"),
    (r"\bSpeed\b", "Speed"),
    (r"\bHP\b", "HP"),
    (r"\bDefense\b", "Defense"),
    (r"\bDefence\b", "Defence"),
    (r"\bAttack\b", "Attack"),
    (r"\bHas \+10% Movement points\b", "Имеет +10% очков передвижения"),
    (r"\bplus 2\.5% more for every 6 hero levels\b", "+2.5% за каждые 6 ур. героя"),
    (r"\bMoves significantly more efficiently on roads\b", "Значительно эффективнее двигается по дорогам"),
    (r"\bDeals \+10% Damage with spells\b", "Наносит +10% урона заклинаниями"),
    (r"\bplus 1% more for every 2 hero levels\b", "+1% за каждые 2 ур. героя"),
    (r"\bDamage from enemy hero spells is reduced by the same value\b", "Урон вражеских заклинаний героя снижается на то же значение"),
]

SYNERGIES = [
    {"skill": "Offense", "subskill": "Battle March", "requires": "Luck", "effect": "Focus per attack bonus is doubled", "effectRu": "Бонус фокуса за атаку удваивается"},
    {"skill": "Offense", "subskill": "Reality Wardens", "requires": "Nightshade Magic", "effect": "+50% damage vs summoned enemies bonus is doubled", "effectRu": "Бонус +50% урона по призванным врагам удваивается"},
    {"skill": "Offense", "subskill": "One for All", "requires": "Tactics", "effect": "Attack per adjacent enemy bonus is doubled", "effectRu": "Бонус атаки за соседних врагов удваивается"},
    {"skill": "Offense", "subskill": "Raw Energy", "requires": "Sorcery", "effect": "+10% magic damage bonus is doubled", "effectRu": "Бонус +10% маг. урона удваивается"},
    {"skill": "Defence", "subskill": "Hymn to the Martyrs", "requires": "Recruitment", "effect": "Focus when taking damage bonus is doubled", "effectRu": "Бонус фокуса при получении урона удваивается"},
    {"skill": "Defence", "subskill": "Wizard Contract", "requires": "Diplomacy", "effect": "−10% magic damage taken bonus is doubled", "effectRu": "Бонус −10% получаемого маг. урона удваивается"},
    {"skill": "Defence", "subskill": "All for One", "requires": "Tactics", "effect": "Defense per adjacent ally bonus is doubled", "effectRu": "Бонус защиты за соседних союзников удваивается"},
    {"skill": "Defence", "subskill": "Avatar of Toughness", "requires": "Summon Avatar", "effect": "Avatar Defense scaling bonus is doubled", "effectRu": "Бонус защиты аватара удваивается"},
    {"skill": "Battlecraft", "subskill": "Resolve", "requires": "Leadership", "effect": "Extra turn chance per Morale bonus is doubled", "effectRu": "Бонус шанса доп. хода за мораль удваивается"},
    {"skill": "Battlecraft", "subskill": "Larger Than Life", "requires": "Diplomacy", "effect": "Army appears +25% stronger bonus is doubled", "effectRu": "Бонус «армия +25% сильнее» удваивается"},
    {"skill": "Battlecraft", "subskill": "Battle Focus", "requires": "Battle Magic", "effect": "+1 Focus Charge at round start is doubled", "effectRu": "+1 заряд фокуса в начале раунда удваивается"},
    {"skill": "Battlecraft", "subskill": "Manacraft", "requires": "Recruitment", "effect": "Max mana from Attack/Defense bonus is doubled", "effectRu": "Бонус макс. маны от атаки/защиты удваивается"},
    {"skill": "Leadership", "subskill": "Avatar of Fury", "requires": "Summon Avatar", "effect": "Avatar Attack scaling bonus is doubled", "effectRu": "Бонус атаки аватара удваивается"},
    {"skill": "Leadership", "subskill": "Civic Innovation", "requires": "Insight", "effect": "+100% Law points bonus is doubled", "effectRu": "Бонус +100% очков законов удваивается"},
    {"skill": "Leadership", "subskill": "Where the Sun Never Sets", "requires": "Daylight Magic", "effect": "Out-of-zone stat and sight bonus is doubled", "effectRu": "Бонус статов и обзора вне зоны удваивается"},
    {"skill": "Luck", "subskill": "Battle March", "requires": "Offense", "effect": "Focus per attack bonus is doubled", "effectRu": "Бонус фокуса за атаку удваивается"},
    {"skill": "Luck", "subskill": "Long-Sight", "requires": "Scouting", "effect": "+1 sight radius bonus is doubled", "effectRu": "Бонус +1 к обзору удваивается"},
    {"skill": "Luck", "subskill": "Beastly Confidence", "requires": "Primal Magic", "effect": "Lucky Strike chance per Luck bonus is doubled", "effectRu": "Бонус шанса удачного удара за удачу удваивается"},
    {"skill": "Luck", "subskill": "Always Heads", "requires": "Economy", "effect": "+25% gold/resources from piles bonus is doubled", "effectRu": "Бонус +25% золота/ресурсов с куч удваивается"},
    {"skill": "Resistance", "subskill": "Chronic Weakness", "requires": "Nightshade Magic", "effect": "Chronic Weakness effect is doubled", "effectRu": "Эффект хронической слабости удваивается"},
    {"skill": "Resistance", "subskill": "Mage Protector's Authority", "requires": "Battle Magic", "effect": "Defense from Knowledge bonus is doubled", "effectRu": "Бонус защиты от знания удваивается"},
    {"skill": "Tactics", "subskill": "One for All", "requires": "Offense", "effect": "Attack per adjacent enemy bonus is doubled", "effectRu": "Бонус атаки за соседних врагов удваивается"},
    {"skill": "Tactics", "subskill": "All for One", "requires": "Defence", "effect": "Defense per adjacent ally bonus is doubled", "effectRu": "Бонус защиты за соседних союзников удваивается"},
    {"skill": "Tactics", "subskill": "Elite Guards", "requires": "Recruitment", "effect": "T1–T3 Attack/Defense bonus is doubled", "effectRu": "Бонус атаки/защиты T1–T3 удваивается"},
    {"skill": "Tactics", "subskill": "Endless Charisma", "requires": "Insight", "effect": "+1 to all stats bonus is doubled", "effectRu": "Бонус +1 ко всем статам удваивается"},
    {"skill": "Recruitment", "subskill": "Manacraft", "requires": "Battlecraft", "effect": "Max mana from Attack/Defense bonus is doubled", "effectRu": "Бонус макс. маны от атаки/защиты удваивается"},
    {"skill": "Recruitment", "subskill": "Hymn to the Martyrs", "requires": "Defence", "effect": "Focus when taking damage bonus is doubled", "effectRu": "Бонус фокуса при получении урона удваивается"},
    {"skill": "Recruitment", "subskill": "Elite Guards", "requires": "Tactics", "effect": "T1–T3 Attack/Defense bonus is doubled", "effectRu": "Бонус атаки/защиты T1–T3 удваивается"},
    {"skill": "Recruitment", "subskill": "Veterans", "requires": "Diplomacy", "effect": "T4 growth +2 bonus is doubled", "effectRu": "Бонус роста T4 +2 удваивается"},
    {"skill": "Wisdom", "subskill": "Familiar Paths", "requires": "Scouting", "effect": "+10 MP at day start in owned zone is doubled", "effectRu": "Бонус +10 ОД при старте дня в своей зоне удваивается"},
    {"skill": "Wisdom", "subskill": "Sticky Magic", "requires": "Sorcery", "effect": "Hero effect duration +2 rounds is doubled", "effectRu": "Бонус +2 раунда к эффектам героя удваивается"},
    {"skill": "Wisdom", "subskill": "Rhythmic Cadence", "requires": "Sorcery", "effect": "+30% max mana bonus is doubled", "effectRu": "Бонус +30% макс. маны удваивается"},
    {"skill": "Wisdom", "subskill": "Stargazer", "requires": "Scouting", "effect": "+250 Astrology Points/day is doubled", "effectRu": "Бонус +250 очков астрологии/день удваивается"},
    {"skill": "Wisdom", "subskill": "Seeing Through", "requires": "Combat", "effect": "Heroic Strike vs temporary units synergy", "effectRu": "Синергия Героического удара с временными юнитами"},
    {"skill": "Battle Magic", "subskill": "Battle Focus", "requires": "Battlecraft", "effect": "+1 Focus Charge at round start is doubled", "effectRu": "+1 заряд фокуса в начале раунда удваивается"},
    {"skill": "Battle Magic", "subskill": "Chaos Reigns", "requires": "Primal Magic", "effect": "Chaos Reigns effect is doubled", "effectRu": "Эффект царства хаоса удваивается"},
    {"skill": "Battle Magic", "subskill": "Battle Mage's Authority", "requires": "Sorcery", "effect": "Attack +20% from Spell Power is doubled", "effectRu": "Бонус атаки +20% от силы заклинаний удваивается"},
    {"skill": "Battle Magic", "subskill": "Mage Protector's Authority", "requires": "Resistance", "effect": "Defense +20% from Knowledge is doubled", "effectRu": "Бонус защиты +20% от знания удваивается"},
    {"skill": "Sorcery", "subskill": "Raw Energy", "requires": "Offense", "effect": "+10% magic damage bonus is doubled", "effectRu": "Бонус +10% маг. урона удваивается"},
    {"skill": "Sorcery", "subskill": "Battle Mage's Authority", "requires": "Battle Magic", "effect": "Attack +20% from Spell Power is doubled", "effectRu": "Бонус атаки +20% от силы заклинаний удваивается"},
    {"skill": "Sorcery", "subskill": "Rhythmic Cadence", "requires": "Wisdom", "effect": "+30% max mana bonus is doubled", "effectRu": "Бонус +30% макс. маны удваивается"},
    {"skill": "Sorcery", "subskill": "Sticky Magic", "requires": "Wisdom", "effect": "Hero effect duration +2 rounds is doubled", "effectRu": "Бонус +2 раунда к эффектам героя удваивается"},
    {"skill": "Summon Avatar", "subskill": "Avatar of Fury", "requires": "Leadership", "effect": "Avatar Attack scaling bonus is doubled", "effectRu": "Бонус атаки аватара удваивается"},
    {"skill": "Summon Avatar", "subskill": "Avatar of Toughness", "requires": "Defence", "effect": "Avatar Defense scaling bonus is doubled", "effectRu": "Бонус защиты аватара удваивается"},
    {"skill": "Summon Avatar", "subskill": "Avatar of Celerity", "requires": "Insight", "effect": "Avatar Speed/Initiative +2 is doubled", "effectRu": "Бонус скорости/инициативы аватара удваивается"},
    {"skill": "Summon Avatar", "subskill": "All Life is Endless", "requires": "Arcane Magic", "effect": "Summon Avatar synergy effect is doubled", "effectRu": "Синергия призыва аватара удваивается"},
    {"skill": "Daylight Magic", "subskill": "Speed of Light", "requires": "Logistics", "effect": "+10 Movement points bonus is doubled", "effectRu": "Бонус +10 ОД удваивается"},
    {"skill": "Daylight Magic", "subskill": "Where the Sun Never Sets", "requires": "Leadership", "effect": "Out-of-zone stat and sight bonus is doubled", "effectRu": "Бонус статов и обзора вне зоны удваивается"},
    {"skill": "Daylight Magic", "subskill": "Scholar Synergy: Arina", "requires": "Nightshade Magic", "effect": "Cross-school spell synergy is doubled", "effectRu": "Межшкольная синергия заклинаний удваивается"},
    {"skill": "Nightshade Magic", "subskill": "Reality Wardens", "requires": "Offense", "effect": "+50% damage vs summoned enemies bonus is doubled", "effectRu": "Бонус +50% урона по призванным врагам удваивается"},
    {"skill": "Nightshade Magic", "subskill": "Chronic Weakness", "requires": "Resistance", "effect": "Chronic Weakness effect is doubled", "effectRu": "Эффект хронической слабости удваивается"},
    {"skill": "Nightshade Magic", "subskill": "Scholar Synergy: Naira", "requires": "Arcane Magic", "effect": "Cross-school spell synergy is doubled", "effectRu": "Межшкольная синергия заклинаний удваивается"},
    {"skill": "Arcane Magic", "subskill": "Careful Planning", "requires": "Logistics", "effect": "Carry over up to 50 unused MP is doubled", "effectRu": "Перенос до 50 неиспользованных ОД удваивается"},
    {"skill": "Arcane Magic", "subskill": "All Life is Endless", "requires": "Summon Avatar", "effect": "Summon Avatar synergy effect is doubled", "effectRu": "Синергия призыва аватара удваивается"},
    {"skill": "Arcane Magic", "subskill": "Scholar Synergy: Doreath", "requires": "Primal Magic", "effect": "Cross-school spell synergy is doubled", "effectRu": "Межшкольная синергия заклинаний удваивается"},
    {"skill": "Primal Magic", "subskill": "Beastly Confidence", "requires": "Luck", "effect": "Lucky Strike chance per Luck bonus is doubled", "effectRu": "Бонус шанса удачного удара за удачу удваивается"},
    {"skill": "Primal Magic", "subskill": "Chaos Reigns", "requires": "Battle Magic", "effect": "Chaos Reigns effect is doubled", "effectRu": "Эффект царства хаоса удваивается"},
    {"skill": "Primal Magic", "subskill": "Scholar Synergy: Hksmilla", "requires": "Daylight Magic", "effect": "Cross-school spell synergy is doubled", "effectRu": "Межшкольная синергия заклинаний удваивается"},
    {"skill": "Logistics", "subskill": "Tax Collector", "requires": "Economy", "effect": "+250 gold/day bonus is doubled", "effectRu": "Бонус +250 золота/день удваивается"},
    {"skill": "Logistics", "subskill": "Speed of Light", "requires": "Daylight Magic", "effect": "+10 Movement points bonus is doubled", "effectRu": "Бонус +10 ОД удваивается"},
    {"skill": "Logistics", "subskill": "Strong Mounts", "requires": "Scouting", "effect": "Neutral global spells −4 mana is doubled", "effectRu": "Бонус −4 маны на нейтральные глобальные заклинания удваивается"},
    {"skill": "Logistics", "subskill": "Careful Planning", "requires": "Arcane Magic", "effect": "Carry over up to 50 unused MP is doubled", "effectRu": "Перенос до 50 неиспользованных ОД удваивается"},
    {"skill": "Scouting", "subskill": "Long-Sight", "requires": "Luck", "effect": "+1 sight radius bonus is doubled", "effectRu": "Бонус +1 к обзору удваивается"},
    {"skill": "Scouting", "subskill": "Familiar Paths", "requires": "Wisdom", "effect": "+10 MP at day start in owned zone is doubled", "effectRu": "Бонус +10 ОД при старте дня в своей зоне удваивается"},
    {"skill": "Scouting", "subskill": "Strong Mounts", "requires": "Logistics", "effect": "Neutral global spells −4 mana is doubled", "effectRu": "Бонус −4 маны на нейтральные глобальные заклинания удваивается"},
    {"skill": "Scouting", "subskill": "Stargazer", "requires": "Wisdom", "effect": "+250 Astrology Points/day is doubled", "effectRu": "Бонус +250 очков астрологии/день удваивается"},
    {"skill": "Diplomacy", "subskill": "Larger Than Life", "requires": "Battlecraft", "effect": "Army appears +25% stronger bonus is doubled", "effectRu": "Бонус «армия +25% сильнее» удваивается"},
    {"skill": "Diplomacy", "subskill": "Veterans", "requires": "Recruitment", "effect": "T4 growth +2 bonus is doubled", "effectRu": "Бонус роста T4 +2 удваивается"},
    {"skill": "Diplomacy", "subskill": "Wizard Contract", "requires": "Defence", "effect": "−10% magic damage taken bonus is doubled", "effectRu": "Бонус −10% получаемого маг. урона удваивается"},
    {"skill": "Diplomacy", "subskill": "Art of the Deal", "requires": "Economy", "effect": "−15% hire cost bonus is doubled", "effectRu": "Бонус −15% стоимости найма удваивается"},
    {"skill": "Economy", "subskill": "Tax Collector", "requires": "Logistics", "effect": "+250 gold/day bonus is doubled", "effectRu": "Бонус +250 золота/день удваивается"},
    {"skill": "Economy", "subskill": "Always Heads", "requires": "Luck", "effect": "+25% gold/resources from piles bonus is doubled", "effectRu": "Бонус +25% золота/ресурсов с куч удваивается"},
    {"skill": "Economy", "subskill": "Art of the Deal", "requires": "Diplomacy", "effect": "−15% hire cost bonus is doubled", "effectRu": "Бонус −15% стоимости найма удваивается"},
    {"skill": "Economy", "subskill": "Experimenter", "requires": "Insight", "effect": "+5 Alchemical Dust bonus is doubled", "effectRu": "Бонус +5 алхимической пыли удваивается"},
    {"skill": "Insight", "subskill": "Avatar of Celerity", "requires": "Summon Avatar", "effect": "Avatar Speed/Initiative +2 is doubled", "effectRu": "Бонус скорости/инициативы аватара удваивается"},
    {"skill": "Insight", "subskill": "Civic Innovation", "requires": "Leadership", "effect": "+100% Law points bonus is doubled", "effectRu": "Бонус +100% очков законов удваивается"},
    {"skill": "Insight", "subskill": "Experimenter", "requires": "Economy", "effect": "+5 Alchemical Dust bonus is doubled", "effectRu": "Бонус +5 алхимической пыли удваивается"},
    {"skill": "Insight", "subskill": "Endless Charisma", "requires": "Tactics", "effect": "+1 to all stats bonus is doubled", "effectRu": "Бонус +1 ко всем статам удваивается"},
    {"skill": "Combat", "subskill": "Inspiring Strike", "requires": "Leadership", "effect": "Heroic Strike cooldown reset synergy", "effectRu": "Синергия сброса перезарядки Героического удара"},
    {"skill": "Combat", "subskill": "Seeing Through", "requires": "Wisdom", "effect": "Heroic Strike vs temporary units synergy", "effectRu": "Синергия Героического удара с временными юнитами"},
]


def norm_skill(skill: str) -> str:
    return SKILL_ALIAS.get(skill, skill)


GROWTH_RE = re.compile(
    r"^(?P<unit>.+?) growth in your cities increases by 1\. Under (?:her|his) command, (?P<unit_cmd>.+?) gain 1 Speed, 1 Initiative, and 20% HP\. "
    r"Their Attack and Defen[cs]e increase by 1 for every 3 hero levels, and enemy (?P<unit_enemy>.+?) lose an equal amount of Attack and Defen[cs]e\.$",
    re.I,
)
RESOURCE_RE = re.compile(
    r"^Produces \+1 (?P<res>Gem|Gems|Crystals?) per day, plus another \+1 for every 5 hero levels\. Increases the amount of (?P<res_map>Gems|Crystals?) found on the map by 100%\.$",
    re.I,
)

SPECIALTY_RU = {
    "ister": "Имеет +10% очков передвижения и ещё +2.5% за каждые 6 ур. героя. Значительно эффективнее двигается по дорогам.",
    "leon-sticky-fingers": "Герой получает +1 к радиусу обзора и ещё +1 за каждые 5 ур. героя.",
    "aeos-the-exalted": "Все союзники получают +1 Morale. Шанс дополнительного хода +2% за пункт Morale и ещё +1% за каждые 4 ур. героя.",
    "lord-edgar": "Союзники получают 20% Attack и Defense героя (как Attack и Defense) и ещё +5% за каждые 6 ур. героя.",
    "old-lord-mandall": "Героический удар наносит +10 базового урона и ещё +5 за каждые 6 ур. героя.",
    "pip": "При повышении уровня получает +1 к случайной характеристике за каждые 2 ур. героя. +5% опыта за каждые 2 ур. героя.",
    "merry-elias": "+1 слот глобального заклинания за каждое изученное глобальное заклинание. Максимальная мана +10% и ещё +5% за каждые 5 ур. героя.",
    "clarissa": "+500 золота/день и ещё +250 за каждые 5 ур. героя.",
    "tarius": "Универсальный герой Necropolis. Начинает с продвинутой Necromancy.",
    "funerella": "Универсальный герой Necropolis. Начинает с продвинутой Necromancy.",
    "mara-matha": "Универсальный герой Schism. Начинает с продвинутой Abyssal Communion.",
    "dh-vri": "Универсальный герой Schism. Начинает с продвинутой Abyssal Communion.",
    "tellaris-the-betrayed": "Начинает с Masterful Early Start — версия не снимается. При касте эффективная сила заклинаний +1 за каждые 3 ур. героя.",
    "stinger": "Героический удар наносит +10 базового урона и ещё +5 за каждые 6 ур. героя.",
    "gorel-spearhead": "Существа армии наносят +10% урона базовых атак и +1% за каждые 2 ур. героя. Дополнительно +1% урона Ranged/Long Reach за каждые 2 ур. героя.",
    "faleor": "Начинает с Masterful Fireball — увеличенная область. При касте эффективная сила заклинаний +1 за каждые 3 ур. героя.",
    "old-pilgrim": "Начинает с Masterful Guillotine — урон растёт вдвое быстрее при повторном касте на одну цель. При касте эффективная сила заклинаний +1 за каждые 3 ур. героя.",
    "elder-tsskish": "Рост Herbomancer в городах +1/нед. Под его командованием Herbomancer получают +1 Speed, +1 Initiative и +20% HP. Attack и Defence +1 за каждые 3 ур. героя; у вражеских Herbomancer — на столько же меньше.",
    "the-minstrel": "В начале каждого раунда генерирует +2 Focus и ещё +1 за каждые 3 ур. героя. Враг теряет столько же Focus.",
    "niev": "Существа армии наносят +10% урона базовых атак и +1% за каждые 2 ур. героя. Дополнительно +1% урона Ranged/Long Reach за каждые 2 ур. героя.",
    "nihil": "Имеет +10% очков передвижения и ещё +2.5% за каждые 6 ур. героя. Значительно эффективнее двигается по дорогам.",
    "blackhorn": "Наносит +10% урона заклинаниями и +1% за каждые 2 ур. героя. Урон вражеских заклинаний героя снижается на то же значение.",
    "eith": "Движение без штрафов местности. +1 к радиусу обзора и ещё +1 за каждые 5 ур. героя.",
    "octavia": "+1 Luck. Союзники получают +2% шанса Lucky Strike за пункт Luck; бонус +1% за каждые 4 ур. героя.",
    "aunt-daliar": "При повышении уровня +1 к случайной характеристике за каждые 2 ур. героя. +5% опыта за каждые 2 ур. героя.",
    "rhea": "Герой и армия получают +1 Luck и ещё +1 за каждые 6 ур. героя.",
    "guildmaster-klastor": "Герой и армия получают +1 Luck и ещё +1 за каждые 6 ур. героя.",
    "kelarr-son-of-navarr": "Герой получает +20% опыта и ещё +5% за каждые 4 ур. героя.",
    "maelstrom": "Герой получает +20% опыта и ещё +5% за каждые 4 ур. героя.",
    "adhan": "Герой получает +20% опыта и ещё +5% за каждые 4 ур. героя.",
    "gleard-the-grey": "Заклинания Arcane Magic, которыми кастует герой, считаются на +1 уровень выше.",
    "lodos": "Заклинания Nightshade Magic, которыми кастует герой, считаются на +1 уровень выше.",
    "sunny-rauktol": "Заклинания Daylight Magic, которыми кастует герой, считаются на +1 уровень выше.",
    "khariseth": "Заклинания Primal Magic, которыми кастует герой, считаются на +1 уровень выше.",
    "mag": "Заклинания Arcane Magic, которыми кастует герой, считаются на +1 уровень выше.",
    "shadespinner-oona": "Заклинания Nightshade Magic, которыми кастует герой, считаются на +1 уровень выше.",
    "martyr-tho": "Заклинания Daylight Magic, которыми кастует герой, считаются на +1 уровень выше.",
    "grellekh-the-betrayer": "Заклинания Nightshade Magic, которыми кастует герой, считаются на +1 уровень выше.",
    "radavok": "Заклинания Arcane Magic, которыми кастует герой, считаются на +1 уровень выше.",
    "lia-the-untethered-one": "Заклинания Daylight Magic, которыми кастует герой, считаются на +1 уровень выше.",
    "sister-deira": "Arina's Chosen усилен и масштабируется с уровнем героя.",
    "anastasia-the-meek": "Arina's Touch усилен и масштабируется с уровнем героя.",
    "oriax": "Summon Avatar усилен и масштабируется с уровнем героя.",
    "the-eye-collective": "Summon Avatar усилен и масштабируется с уровнем героя.",
    "julius": "Healing Water восстанавливает дополнительное HP в зависимости от уровня героя и лечит больше отрядов.",
    "nadir": "Vulnerability снижает Defense врагов эффективнее и масштабируется с уровнем героя.",
    "vesper": "Blessing даёт дополнительные Attack и Defense, растущие с уровнем героя.",
    "zoran-the-self-founded": "Начинает только с Waurms. Уникальная специализация на состав армии.",
    "batham": "+1 кристалл/день и ещё +1 за каждые 5 ур. героя. Количество кристаллов на карте увеличено на 100%.",
    "curson-duke-of-rage": "Существа наносят повышенный урон при срабатывании Morale.",
    "carth": "Специалист по блокировке и контролю Primal Magic.",
    "orex": "Бонусы Summon Avatar и мобильности в стиле blink.",
    "kelghul": "Существа T6 в армии получают +1 Speed, +1 Initiative и +20% HP. Их Attack и Defence +1 за каждые 3 ур. героя.",
}


MAGIC_SCHOOL_RE = re.compile(
    r"^(?P<school>.+ Magic) spells cast by the hero are treated as \+1 level higher\.$",
    re.I,
)


def translate_ru(text: str, hero_id: str | None = None) -> str:
    if hero_id and hero_id in SPECIALTY_RU:
        return SPECIALTY_RU[hero_id]
    mm = MAGIC_SCHOOL_RE.match(text)
    if mm:
        return f"Заклинания {mm.group('school')}, которыми кастует герой, считаются на +1 уровень выше."
    m = GROWTH_RE.match(text)
    if m:
        unit = m.group("unit_cmd")
        return (
            f"Рост {m.group('unit')} в городах +1/нед. Под командованием героя {unit} получают +1 Speed, +1 Initiative и +20% HP. "
            f"Их Attack и Defence +1 за каждые 3 ур. героя; у вражеских {m.group('unit_enemy')} Attack и Defence снижаются на столько же."
        )

    rm = RESOURCE_RE.match(text)
    if rm:
        res_key = rm.group("res")
        if "Crystal" in res_key:
            res, res_pl = "кристалл", "кристаллов"
        else:
            res, res_pl = "самоцвет", "самоцветов"
        return (
            f"+1 {res}/день и ещё +1 за каждые 5 ур. героя. "
            f"Количество {res_pl} на карте увеличено на 100%."
        )

    if re.match(r"^The hero gains \+20% XP, plus 5% more for every 4 hero levels\.$", text):
        return "Герой получает +20% опыта и ещё +5% за каждые 4 ур. героя."
    if re.match(r"^The hero and army gain \+1 Luck, plus \+1 more for every 6 hero levels\.$", text):
        return "Герой и армия получают +1 Luck и ещё +1 за каждые 6 ур. героя."
    if re.match(r"^Produces \+1 Crystal per day, plus another \+1 for every 5 hero levels\.$", text, re.I):
        return "+1 кристалл/день и ещё +1 за каждые 5 ур. героя."
    if " is improved and scales with hero level" in text:
        name = text.split(" is improved")[0]
        return f"{name} усилен и масштабируется с уровнем героя."

    out = text
    for pattern, repl in RU_TERMS:
        out = re.sub(pattern, repl, out, flags=re.I)
    return out


def build_start(hero: dict) -> list[dict]:
    skills = [{"skill": norm_skill(s["skill"]), "tier": s["tier"]} for s in hero["startingSkills"]]
    hid = hero["id"]
    faction_skill = FACTION_SKILL[hero["faction"]]

    if hid in UNIVERSAL_IDS:
        adv = [s for s in skills if s["skill"] == faction_skill and s["tier"] == "Advanced"]
        return adv if adv else skills

    secondary = [s for s in skills if not (s["skill"] == faction_skill and s["tier"] == "Basic")]
    if secondary:
        return secondary
    return skills


def transform_hero(raw: dict, overrides: dict, ru_overrides: dict) -> dict:
    hid = raw["id"]
    spec_name = raw["specialty"]["name"]
    spec_desc = overrides.get(hid) or raw["specialty"]["description"]
    if len(spec_desc) < 40 and "specialization for" in spec_desc:
        spec_desc = overrides.get(hid, spec_desc)

    out = {
        "id": hid,
        "name": raw["name"],
        "faction": raw["faction"],
        "class": raw["class"],
        "specialty": spec_name,
        "specialtyDesc": spec_desc,
        "specialtyDescEn": spec_desc,
        "specialtyDescRu": ru_overrides.get(hid) or translate_ru(spec_desc, hid),
        "start": build_start(raw),
        "universal": hid in UNIVERSAL_IDS,
    }

    if raw["name"] in NAME_RU:
        out["nameRu"] = NAME_RU[raw["name"]]

    if raw.get("startingSpell"):
        out["spell"] = raw["startingSpell"]

    if hid in HERO_SUBCLASS_HINTS:
        out["subclassHint"] = HERO_SUBCLASS_HINTS[hid]

    return out


def main() -> None:
    (ROOT / "synergies.json").write_text(json.dumps(SYNERGIES, ensure_ascii=False, indent=2), encoding="utf-8")

    syn_js = []
    for s in SYNERGIES:
        syn_js.append({
            **s,
            "sub": s["subskill"],
            "needs": s["requires"],
            "descEn": s["effect"],
            "descRu": s["effectRu"],
        })
    (ROOT / "hero-builder-synergies.js").write_text(
        "/* Auto-generated by build_hero_builder_export.py */\n"
        f"window.HOE_BUILDER_SYNERGIES = {json.dumps(syn_js, ensure_ascii=False, indent=2)};\n",
        encoding="utf-8",
    )

    print(f"Exported {len(SYNERGIES)} synergies")


if __name__ == "__main__":
    main()
