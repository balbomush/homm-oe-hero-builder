#!/usr/bin/env python3
"""Build HoMM OE heroes.json from compiled wiki/fandom/community data."""
import json
import re

def slug(name):
    s = name.lower()
    s = s.replace("'", "").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def hero(name, faction, cls, htype, spec_name, spec_desc, skills, spell=None,
         subclass=None, adv_faction=False):
    o = {
        "id": slug(name),
        "name": name,
        "faction": faction,
        "class": cls,
        "type": htype,
        "specialty": {"name": spec_name, "description": spec_desc},
        "startingSkills": skills,
        "advancedFactionSkill": adv_faction,
    }
    if spell:
        o["startingSpell"] = spell
    if subclass:
        o["subclassAdvantage"] = subclass
    return o

# Faction skill names
FS = {
    "Temple": "Righteousness",
    "Necropolis": "Necromancy",
    "Dungeon": "Triumvirate's Strength",
    "Grove": "Murmuring",
    "Hive": "Summon Swarm",
    "Schism": "Abyssal Communion",
}

def fs(faction, tier="Basic"):
    return {"skill": FS[faction], "tier": tier}

heroes = []

# --- TEMPLE (18) ---
# Knights
heroes += [
    hero("Ister", "Temple", "Knight", "Might", "Wayfarer",
         "Has +10% Movement points, plus 2.5% more for every 6 hero levels. Moves significantly more efficiently on roads.",
         [fs("Temple"), {"skill": "Logistics", "tier": "Basic"}]),
    hero("Leon Sticky-Fingers", "Temple", "Knight", "Might", "Scout",
         "Increases sight radius and map mobility for scouting.",
         [fs("Temple"), {"skill": "Scouting", "tier": "Basic"}]),
    hero("John Johnson", "Temple", "Knight", "Might", "Defender",
         "Defensive combat specialist.",
         [fs("Temple"), {"skill": "Defence", "tier": "Basic"}]),
    hero("Kestrel", "Temple", "Knight", "Might", "Jaeger",
         "Crossbowmen growth in your cities increases by 1. Under her command, Crossbowmen gain 1 Speed, 1 Initiative, and 20% HP. Their Attack and Defence increase by 1 for every 3 hero levels, and enemy Crossbowmen lose an equal amount of Attack and Defence.",
         [fs("Temple"), {"skill": "Offense", "tier": "Basic"}], subclass="Offense"),
    hero("Aeos the Exalted", "Temple", "Knight", "Might", "Morale Master",
         "Morale-focused knight who punishes enemies via the morale system.",
         [fs("Temple"), {"skill": "Leadership", "tier": "Basic"}], subclass="Leadership"),
    hero("Heretic Avis", "Temple", "Knight", "Might", "Recruiter",
         "Focuses on recruitment and army gathering.",
         [fs("Temple"), {"skill": "Recruitment", "tier": "Basic"}]),
    hero("Keandra", "Temple", "Knight", "Might", "Cavalry Tactician",
         "Strong cavalry tactics focus.",
         [fs("Temple"), {"skill": "Battlecraft", "tier": "Basic"}], subclass="Battlecraft"),
    hero("Lord Edgar", "Temple", "Knight", "Might", "True Lord",
         "Friendly creatures gain 20% of his Attack and Defense (as Attack and Defense), plus another 5% for every 6 hero levels.",
         [{"skill": "Righteousness", "tier": "Advanced"}], adv_faction=True),
    hero("Old Lord Mandall", "Temple", "Knight", "Might", "Resistant",
         "Defensive kit focused on resistance.",
         [fs("Temple"), {"skill": "Resistance", "tier": "Basic"}]),
]
# Clerics
heroes += [
    hero("Merry Elias", "Temple", "Cleric", "Magic", "Diplomat",
         "Diplomacy-focused support cleric.",
         [fs("Temple"), {"skill": "Diplomacy", "tier": "Basic"}]),
    hero("Pip", "Temple", "Cleric", "Magic", "Wish to Learn",
         "When leveling up, gains 1 additional attribute point(s) for every 2 hero levels. Gains +5% XP for every 2 hero levels.",
         [fs("Temple"), {"skill": "Insight", "tier": "Basic"}], subclass="Insight"),
    hero("Zenith", "Temple", "Cleric", "Magic", "Lightweaver",
         "Starts with strong early-tier units; intelligence focus.",
         [fs("Temple"), {"skill": "Intelligence", "tier": "Basic"}]),
    hero("Lia the Untethered One", "Temple", "Cleric", "Magic", "Untethered Caster",
         "Daylight magic specialist; support caster.",
         [fs("Temple"), {"skill": "Daylight Magic", "tier": "Basic"}]),
    hero("Julius", "Temple", "Cleric", "Magic", "Ascendant Path",
         "High probability of reaching the Ascendant subclass path.",
         [fs("Temple"), {"skill": "Resistance", "tier": "Basic"}], subclass="Resistance"),
    hero("Vesper", "Temple", "Cleric", "Magic", "Daylight Adept",
         "Secondary daylight magic caster.",
         [fs("Temple"), {"skill": "Daylight Magic", "tier": "Basic"}]),
    hero("Anastasia the Meek", "Temple", "Cleric", "Magic", "Thaumaturge",
         "Thaumaturgy utility caster.",
         [fs("Temple"), {"skill": "Thaumaturgy", "tier": "Basic"}]),
    hero("Nadir", "Temple", "Cleric", "Magic", "Nightshade Dabbler",
         "Nightshade magic; weak faction synergy.",
         [fs("Temple"), {"skill": "Nightshade Magic", "tier": "Basic"}]),
    hero("Clarissa", "Temple", "Cleric", "Magic", "Economist",
         "Passive gold income generator.",
         [fs("Temple"), {"skill": "Economy", "tier": "Basic"}], subclass="Economy"),
]

# --- NECROPOLIS (18) ---
dk = [
    ("Bulwark", "Bulwark", "Defence", "Defence", "Walking Rot"),
    ("King-of-Kings", "Royal Diplomat", "Diplomacy", "Diplomacy", "Walking Rot"),
    ("Onkos", "Onkos", "Offense", "Offense", None),
    ("Kel'Ghul", "Dread Knight", "Tactics", "Tactics", "Walking Rot"),
    ("Natalida", "Scout of Shadowspire", "Scouting", "Scouting", "Harbinger of Doom"),
    ("Artorius Veritas", "Truth Seeker", "Resistance", "Resistance", "Walking Rot"),
    ("Marl", "Marl", "Logistics", "Logistics", None),
    ("Tarius", "Tarius", "Necromancy", "Necromancy", None),
    ("Zam", "Zam", "Battlecraft", "Battlecraft", None),
]
for name, spec, skill, sub, subadv in dk:
    tier = "Advanced" if skill == "Necromancy" and name == "Tarius" else "Basic"
    heroes.append(hero(name, "Necropolis", "Death Knight", "Might", spec,
         f"{spec} specialization for Death Knight.",
         [{"skill": "Necromancy", "tier": tier}, {"skill": skill if skill != "Necromancy" else "Battlecraft", "tier": "Basic"}],
         subclass=subadv, adv_faction=(name == "Tarius")))

nc = [
    ("Mag", "Mag", "Arcane Magic", "Soulweaver"),
    ("Adhan", "Adhan", "Insight", "Insight"),
    ("Ethric", "Ethric", "Intelligence", None),
    ("Guildmaster Klastor", "Guildmaster", "Luck", None),
    ("Shadespinner Oona", "Shadespinner", "Nightshade Magic", None),
    ("Laura", "Laura", "Sorcery", None),
    ("Lord Rufus", "Lord Rufus", "Thaumaturgy", None),
    ("Funerella", "Funerella", "Necromancy", None),
    ("Milossa the Golden", "Milossa", "Battle Magic", "Chronomancer"),
]
for name, spec, skill, subadv in nc:
    tier = "Advanced" if name == "Funerella" else "Basic"
    second = skill if skill != "Necromancy" else "Arcane Magic"
    heroes.append(hero(name, "Necropolis", "Necromancer", "Magic", spec,
         f"{spec} specialization for Necromancer.",
         [{"skill": "Necromancy", "tier": tier}, {"skill": second, "tier": "Basic"}],
         subclass=subadv, adv_faction=(name == "Funerella")))

# Fix Tarius and Funerella skills properly
for h in heroes:
    if h["id"] == "tarius":
        h["startingSkills"] = [{"skill": "Necromancy", "tier": "Advanced"}, {"skill": "Battlecraft", "tier": "Basic"}]
        h["advancedFactionSkill"] = True
    if h["id"] == "funerella":
        h["startingSkills"] = [{"skill": "Necromancy", "tier": "Advanced"}]
        h["advancedFactionSkill"] = True

# --- DUNGEON (18) ---
overlords = [
    ("Enatee", "Slitering Menace", "Defence", "Defence"),
    ("Tellaris the Betrayed", "Early Start", "Early Start", "Early Start", "Early Start"),
    ("Stinger", "Stinger", "Triumvirate's Strength", None, True),
    ("Kieran", "Kieran", "Offense", None),
    ("Mouaren", "Mouaren", "Scouting", "Scouting"),
    ("Devir, Son of Devir", "Devir", "Leadership", "Leadership"),
    ("Creta, Daughter of Navarr", "Creta", "Offense", None),
    ("Rhea", "Rhea", "Luck", "Luck"),
    ("Gleard the Grey", "Gleard", "Defence", None),
]
for entry in overlords:
  if len(entry) == 5:
    name, spec, sk, sub, adv = entry
  else:
    name, spec, sk, sub = entry
    adv = False
  if adv:
    skills = [{"skill": "Triumvirate's Strength", "tier": "Advanced"}]
    heroes.append(hero(name, "Dungeon", "Overlord", "Might", spec,
         f"{spec} — Overlord specialty.", skills, adv_faction=True))
  else:
    heroes.append(hero(name, "Dungeon", "Overlord", "Might", spec,
         f"{spec} — Overlord specialty.",
         [fs("Dungeon"), {"skill": sk, "tier": "Basic"}], subclass=sub,
         spell="Early Start" if "Early Start" in spec else None))

# Fix Tellaris
for h in heroes:
    if h["id"] == "tellaris-the-betrayed":
        h["startingSkills"] = [fs("Dungeon"), {"skill": "Battlecraft", "tier": "Basic"}]
        h["startingSpell"] = "Early Start"
        h["advancedFactionSkill"] = False
        h["specialty"] = {"name": "Early Start", "description": "With One Eye Open — Starts with the Masterful Early Start spell. This version cannot be dispelled. While casting, effective Spell Power increases by 1 for every 3 hero levels."}

warlocks = [
    ("Kelarr, Son of Navarr", "Kelarr", "Insight", "Insight"),
    ("Zakron the Great", "Zakron", "Arcane Magic", None),
    ("Sister Deira", "Sister Deira", "Daylight Magic", None),
    ("Motley", "Motley", "Sorcery", None),
    ("Ylwari", "Ylwari", "Nightshade Magic", None),
    ("Glastor", "Glastor", "Economy", "Economy"),
    ("Typhona", "Typhona", None, None, True),
    ("Sunny Rauktol", "Sunny Rauktol", "Battle Magic", None),
    ("Lodos", "Lodos", "Primal Magic", None),
]
for entry in warlocks:
    if len(entry) == 5:
        name, spec, sk, sub, adv = entry
    else:
        name, spec, sk, sub = entry
        adv = False
    if adv:
        heroes.append(hero(name, "Dungeon", "Warlock", "Magic", spec,
             "Typhona — advanced Triumvirate's Strength Warlock.",
             [{"skill": "Triumvirate's Strength", "tier": "Advanced"}], adv_faction=True))
    else:
        heroes.append(hero(name, "Dungeon", "Warlock", "Magic", spec,
             f"{spec} — Warlock specialty.",
             [fs("Dungeon"), {"skill": sk, "tier": "Basic"}], subclass=sub))

for h in heroes:
    if h["id"] == "stinger":
        h["startingSkills"] = [{"skill": "Triumvirate's Strength", "tier": "Advanced"}, {"skill": "Siegecraft", "tier": "Basic"}]
        h["advancedFactionSkill"] = True
    if h["id"] == "typhona":
        h["startingSkills"] = [{"skill": "Triumvirate's Strength", "tier": "Advanced"}]
        h["advancedFactionSkill"] = True

# --- GROVE (18) ---
wardens = [
    ("Eith", "From A Bird's Eye", "Scouting", None, None),
    ("Gorel Spearhead", "Shooter", "Offense", "Offense", None),
    ("Gingertail", "Faunsong", "Battlecraft", None, None),
    ("Old Pilgrim", "Guillotine Master", "Battle Magic", None, "Guillotine"),
    ("Octavia", "Lucky Commander", "Luck", "Luck", None),
    ("Mreowa", "Crystal Harvest", "Sorcery", None, None),
    ("Alluring Sh'a", "Diplomatic Retainer", "Diplomacy", "Diplomacy", None),
    ("Aunt Daliar", "Wish to Learn", "Insight", "Insight", None),
    ("Faleor", "Hksmilla's Step", "Murmuring", None, "Fireball", True),
]
for w in wardens:
    name, spec, sk, sub, spell = w[0], w[1], w[2], w[3], w[4] if len(w) > 4 else None
    adv = w[5] if len(w) > 5 else False
    if adv:
        skills = [{"skill": "Murmuring", "tier": "Advanced"}]
    else:
        skills = [fs("Grove"), {"skill": sk, "tier": "Basic"}]
    heroes.append(hero(name, "Grove", "Warden", "Might", spec,
         f"{spec} — Warden specialty.", skills, spell=spell, subclass=sub, adv_faction=adv))

druids = [
    ("Vatawna", "Spiritual Vigour", "Wisdom", None, "Primordial Chaos"),
    ("Elder Tss'Kish", "Herbomancer Lord", "Thaumaturgy", None, "Song of Power"),
    ("Aeliniel", "Firewall Adept", "Primal Magic", None, "Firewall"),
    ("Glacia", "Ice Weaver", "Primal Magic", None, "Ice Bolt"),
    ("Vim", "Cave Master", "Primal Magic", None, "Cave In"),
    ("Echolily", "Mirror Mage", "Arcane Magic", "Arcane Magic", "Mirror Copy"),
    ("Sullie", "Avatar Summoner", "Summon Avatar", "Summon Avatar", "Weakening Ray"),
    ("Halon", "Chain Lightning", "Arcane Magic", None, "Chain Lightning"),
    ("The Minstrel", "Wandering Musician", "Sorcery", "Sorcery", "Energy Explosion"),
]
for d in druids:
    name, spec, sk, sub, spell = d[0], d[1], d[2], d[3], d[4]
    heroes.append(hero(name, "Grove", "Druid", "Magic", spec,
         f"{spec} — Druid specialty.",
         [fs("Grove"), {"skill": sk, "tier": "Basic"}], spell=spell, subclass=sub))

# Specialty text overrides (sportskeeda / olden-era)
spec_overrides = {
    "gingertail": ("Faunsong", "Faun growth in your cities increases by 1. Under her command, Fauns gain +1 Speed, +1 Initiative, and +20% HP. Their Attack and Defense increase by 1 for every 3 hero levels, and enemy Fauns lose an equal amount of Attack and Defense."),
    "gorel-spearhead": ("Shooter", "Creatures in his army deal +10% basic attack damage, plus an additional +1% for every 2 hero levels. Additionally, they deal +1% Ranged and Long Reach damage for every 2 hero levels."),
    "faleor": ("Hksmilla's Step", "He starts with the Masterful Fireball spell. This version hits a larger area. While casting this spell, effective Spell Power is increased by 1 for every 3 hero levels."),
    "elder-tsskish": ("Herbomancer Growth", "Herbomancer growth in your cities increases by 1. Under his command, Herbomancers gain 1 Speed, 1 Initiative, and 20% HP. Their Attack and Defense increase by 1 for every 3 hero levels, and enemy Herbomancers lose an equal amount of Attack and Defence."),
    "the-minstrel": ("Wandering Musician", "At the beginning of each round, he generates +2 Focus Points, plus an additional +1 for every 3 hero levels. The enemy loses the same amount of Focus Points."),
    "enatee": ("Medusae", "Medusae growth in your cities increases by 1. Under her command, Medusae gain 1 Speed, 1 Initiative, and 20% HP. Their Attack and Defence increase by 1 for every 3 hero levels, and enemy Medusae lose an equal amount of Attack and Defence."),
}
for h in heroes:
    if h["id"] in spec_overrides:
        n, d = spec_overrides[h["id"]]
        h["specialty"] = {"name": n, "description": d}

# --- HIVE (18) ---
enforcers = [
    ("Zoran, the Self-Founded", "Self-Founded", "Nightshade Magic", "Nightshade Magic"),
    ("Curson, Duke of Rage", "Duke of Rage", "Battlecraft", None),
    ("Maelstrom", "Reaver Lord", "Insight", "Insight"),
    ("Nor", "Nor", "Battlecraft", "Battlecraft"),
    ("Tavi", "Swarm Lord", "Summon Swarm", None, True),
    ("Low", "Locust Master", "Offense", None),
    ("Goldentongue", "Goldentongue", "Leadership", "Leadership"),
    ("Abigor", "Duke of Battle", "Tactics", None),
    ("Popper", "Speed Commander", "Logistics", None),
]
for e in enforcers:
    name, spec, sk, sub = e[0], e[1], e[2], e[3]
    adv = e[4] if len(e) > 4 else False
    if adv:
        heroes.append(hero(name, "Hive", "Enforcer", "Might", spec,
             "Tavi — advanced Summon Swarm.",
             [{"skill": "Summon Swarm", "tier": "Advanced"}], adv_faction=True))
    else:
        heroes.append(hero(name, "Hive", "Enforcer", "Might", spec,
             f"{spec} — Enforcer specialty.",
             [fs("Hive"), {"skill": sk, "tier": "Basic"}], subclass=sub))

heralds = [
    ("Niev", "Shooter", "Sorcery", None, "Favorable Wind"),
    ("Mila", "Haste Herald", "Primal Magic", None),
    ("Batham", "Crystal Duke", "Economy", None),
    ("Orex", "Blink Master", "Summon Avatar", None),
    ("Carth", "Primal Lock", "Primal Magic", None),
    ("Flu", "Wayfarer", "Logistics", None),
    ("Zur", "Tank", "Resistance", None),
    ("Khariseth", "Khariseth", "Primal Magic", "Primal Magic"),
    ("Oriax", "Oriax", "Summon Avatar", "Summon Avatar"),
]
for h_entry in heralds:
    name, spec, sk, sub = h_entry[0], h_entry[1], h_entry[2], h_entry[3]
    spell = h_entry[4] if len(h_entry) > 4 else None
    heroes.append(hero(name, "Hive", "Herald", "Magic", spec,
         f"{spec} — Herald specialty.",
         [fs("Hive"), {"skill": sk, "tier": "Basic"}], spell=spell, subclass=sub))

for h in heroes:
    if h["id"] == "tavi":
        h["startingSkills"] = [{"skill": "Summon Swarm", "tier": "Advanced"}, {"skill": "Battle Magic", "tier": "Basic"}]
    if h["id"] == "niev":
        h["specialty"] = {"name": "Shooter", "description": "All creatures in her army deal +10% basic attack damage, plus 1% more for every 2 hero levels. Additionally, they gain +1% Ranged and Long Reach damage for every 2 hero levels."}

# --- SCHISM (18) ---
oathkeepers = [
    ("Nihil", "Wayfarer", "Logistics", None),
    ("Blackhorn", "Spellweaver", "Sorcery", "Sorcery"),
    ("Matastala the White", "Matastala", "Offense", None),
    ("Jänhei", "Jänhei", "Wisdom", "Wisdom"),
    ("Mara Matha", "Mara Matha", "Abyssal Communion", None, True),
    ("Iron Master", "Iron Master", "Diplomacy", "Diplomacy"),
    ("Walkha", "Walkha", "Battlecraft", None),
    ("Changeling Urgo", "Urgo", "Resistance", None),
    ("Martyr Tho", "Tho", "Daylight Magic", "Daylight Magic"),
]
for o in oathkeepers:
    name, spec, sk, sub = o[0], o[1], o[2], o[3]
    adv = o[4] if len(o) > 4 else False
    if adv:
        heroes.append(hero(name, "Schism", "Oathkeeper", "Might", spec,
             "Starts with Advanced Abyssal Communion.",
             [{"skill": "Abyssal Communion", "tier": "Advanced"}], adv_faction=True))
    else:
        heroes.append(hero(name, "Schism", "Oathkeeper", "Might", spec,
             f"{spec} — Oathkeeper specialty.",
             [fs("Schism"), {"skill": sk, "tier": "Basic"}], subclass=sub))

for h in heroes:
    if h["id"] == "blackhorn":
        h["specialty"] = {"name": "Spellweaver", "description": "Deals +10% Damage with spells, plus 1% more for every 2 hero levels. Damage from enemy hero spells is reduced by the same value."}
    if h["id"] == "nihil":
        h["specialty"] = {"name": "Logistics", "description": "Has +10% Movement points, plus 2.5% more for every 6 hero levels. Moves significantly more efficiently on roads."}

riftspeakers = [
    ("Grellekh the Betrayer", "Betrayer", "Nightshade Magic", None),
    ("Icequeen Hel'Ghat", "Hel'Ghat", "Defence", "Defence"),
    ("Kwinri", "Kwinri", "Battle Magic", None),
    ("The Eye Collective", "Eye Collective", "Summon Avatar", "Summon Avatar"),
    ("Tōlketh", "Tōlketh", "Logistics", "Logistics"),
    ("Ulkuth", "Ulkuth", "Sorcery", None),
    ("Ra'Davok", "Ra'Davok", "Arcane Magic", "Arcane Magic"),
    ("Sister Keiri", "Sister Keiri", "Battlecraft", None),
    ("Dhüvri", "Dhüvri", "Abyssal Communion", None, True),
]
for r in riftspeakers:
    name, spec, sk, sub = r[0], r[1], r[2], r[3]
    adv = r[4] if len(r) > 4 else False
    if adv:
        heroes.append(hero(name, "Schism", "Riftspeaker", "Magic", spec,
             "Starts with Advanced Abyssal Communion.",
             [{"skill": "Abyssal Communion", "tier": "Advanced"}], adv_faction=True))
    else:
        heroes.append(hero(name, "Schism", "Riftspeaker", "Magic", spec,
             f"{spec} — Riftspeaker specialty.",
             [fs("Schism"), {"skill": sk, "tier": "Basic"}], subclass=sub))

# --- CLASSES ---
def skill_chances(pairs):
    return {k: v for k, v in pairs}

classes = {
    "Knight": {
        "faction": "Temple",
        "type": "Might",
        "factionSkill": "Righteousness",
        "statGrowth": {"attack": {"base": 2, "1-12": 0.35, "13+": 0.25}, "defence": {"base": 3, "1-12": 0.35, "13+": 0.25}, "spellPower": {"base": 1, "1-12": 0.15, "13+": 0.25}, "knowledge": {"base": 1, "1-12": 0.15, "13+": 0.25}},
        "skillRollChances": skill_chances([
            ("Offense", 15), ("Defence", 15), ("Resistance", 15), ("Battlecraft", 15),
            ("Sorcery", 5), ("Intelligence", 5), ("Summon Avatar", 5), ("Battle Magic", 5),
            ("Daylight Magic", 8), ("Nightshade Magic", 2), ("Arcane Magic", 6), ("Primal Magic", 4),
            ("Leadership", 15), ("Luck", 5), ("Insight", 10), ("Diplomacy", 10),
            ("Logistics", 10), ("Scouting", 10), ("Economy", 10), ("Tactics", 10),
            ("Siegecraft", 10), ("Recruitment", 10), ("Thaumaturgy", 0),
        ]),
        "subclasses": {
            "Swashbuckler": {"effect": "Heroic Strike deals +200 damage.", "requiredSkillsExpert": ["Leadership", "Nightshade Magic", "Offense", "Luck", "Intelligence"]},
            "Paragon": {"effect": "All allies deal maximum damage and take minimum damage.", "requiredSkillsExpert": ["Daylight Magic", "Battlecraft", "Diplomacy", "Summon Avatar", "Tactics"]},
        },
    },
    "Cleric": {
        "faction": "Temple",
        "type": "Magic",
        "factionSkill": "Righteousness",
        "statGrowth": {"attack": {"base": 1, "1-12": 0.15, "13+": 0.25}, "defence": {"base": 1, "1-12": 0.15, "13+": 0.25}, "spellPower": {"base": 2, "1-12": 0.35, "13+": 0.25}, "knowledge": {"base": 3, "1-12": 0.35, "13+": 0.25}},
        "skillRollChances": skill_chances([
            ("Offense", 5), ("Defence", 5), ("Resistance", 5), ("Battlecraft", 5),
            ("Sorcery", 15), ("Intelligence", 15), ("Summon Avatar", 15), ("Battle Magic", 15),
            ("Daylight Magic", 8), ("Nightshade Magic", 2), ("Arcane Magic", 6), ("Primal Magic", 4),
            ("Leadership", 15), ("Luck", 5), ("Insight", 10), ("Diplomacy", 10),
            ("Logistics", 10), ("Scouting", 10), ("Economy", 10), ("Tactics", 10),
            ("Siegecraft", 10), ("Recruitment", 0), ("Thaumaturgy", 10),
        ]),
        "subclasses": {
            "Grand Inquisitor": {"effect": "Enemy hero can only use each spell once per battle.", "requiredSkillsExpert": ["Arcane Magic", "Battle Magic", "Defence", "Insight", "Scouting"]},
            "Ascendant": {"effect": "All the hero's spells always cost 0 mana.", "requiredSkillsExpert": ["Primal Magic", "Economy", "Logistics", "Resistance", "Sorcery"]},
        },
    },
    "Death Knight": {
        "faction": "Necropolis",
        "type": "Might",
        "factionSkill": "Necromancy",
        "statGrowth": {"attack": {"base": 3, "1-12": 0.45, "13+": 0.25}, "defence": {"base": 1, "1-12": 0.25, "13+": 0.25}, "spellPower": {"base": 1, "1-12": 0.15, "13+": 0.25}, "knowledge": {"base": 2, "1-12": 0.15, "13+": 0.25}},
        "skillRollChances": skill_chances([
            ("Offense", 15), ("Defence", 15), ("Resistance", 15), ("Battlecraft", 15),
            ("Sorcery", 5), ("Intelligence", 5), ("Summon Avatar", 5), ("Battle Magic", 5),
            ("Daylight Magic", 2), ("Nightshade Magic", 8), ("Arcane Magic", 6), ("Primal Magic", 4),
            ("Leadership", 0), ("Luck", 15), ("Insight", 15), ("Diplomacy", 7.5),
            ("Logistics", 10), ("Scouting", 10), ("Economy", 10), ("Tactics", 7.5),
            ("Siegecraft", 10), ("Recruitment", 10), ("Thaumaturgy", 0),
        ]),
        "subclasses": {
            "Harbinger of Doom": {"effect": "Enemy creatures have minimum Luck and always land unlucky strikes.", "requiredSkillsExpert": ["Primal Magic", "Sorcery", "Luck", "Scouting", "Defence"]},
            "Walking Rot": {"effect": "All enemies always have minimum Morale.", "requiredSkillsExpert": ["Nightshade Magic", "Diplomacy", "Intelligence", "Resistance", "Tactics"]},
        },
    },
    "Necromancer": {
        "faction": "Necropolis",
        "type": "Magic",
        "factionSkill": "Necromancy",
        "statGrowth": {"attack": {"base": 1, "1-12": 0.1, "13+": 0.25}, "defence": {"base": 0, "1-12": 0.15, "13+": 0.25}, "spellPower": {"base": 2, "1-12": 0.35, "13+": 0.25}, "knowledge": {"base": 4, "1-12": 0.4, "13+": 0.25}},
        "skillRollChances": skill_chances([
            ("Offense", 5), ("Defence", 5), ("Resistance", 5), ("Battlecraft", 5),
            ("Sorcery", 15), ("Intelligence", 15), ("Summon Avatar", 15), ("Battle Magic", 15),
            ("Daylight Magic", 2), ("Nightshade Magic", 8), ("Arcane Magic", 6), ("Primal Magic", 4),
            ("Leadership", 0), ("Luck", 15), ("Insight", 15), ("Diplomacy", 7.5),
            ("Logistics", 10), ("Scouting", 10), ("Economy", 10), ("Tactics", 7.5),
            ("Siegecraft", 10), ("Recruitment", 0), ("Thaumaturgy", 10),
        ]),
        "subclasses": {
            "Soulweaver": {"effect": "After an enemy stack is killed, a temporary stack of friendly Wights appears.", "requiredSkillsExpert": ["Arcane Magic", "Battlecraft", "Insight", "Logistics", "Summon Avatar"]},
            "Chronomancer": {"effect": "Necromancy works for all creatures, not just Undead.", "requiredSkillsExpert": ["Daylight Magic", "Economy", "Offense", "Tactics", "Battle Magic"]},
        },
    },
    "Overlord": {
        "faction": "Dungeon",
        "type": "Might",
        "factionSkill": "Triumvirate's Strength",
        "statGrowth": {"attack": {"base": 2, "1-12": 0.25, "13+": 0.25}, "defence": {"base": 2, "1-12": 0.3, "13+": 0.25}, "spellPower": {"base": 2, "1-12": 0.25, "13+": 0.25}, "knowledge": {"base": 1, "1-12": 0.2, "13+": 0.25}},
        "skillRollChances": skill_chances([
            ("Offense", 15), ("Defence", 15), ("Resistance", 15), ("Battlecraft", 15),
            ("Sorcery", 5), ("Intelligence", 5), ("Summon Avatar", 5), ("Battle Magic", 5),
            ("Daylight Magic", 5), ("Nightshade Magic", 5), ("Arcane Magic", 5), ("Primal Magic", 5),
            ("Leadership", 12.5), ("Luck", 7.5), ("Insight", 7.5), ("Diplomacy", 12.5),
            ("Logistics", 5), ("Scouting", 12.5), ("Economy", 12.5), ("Tactics", 10),
            ("Siegecraft", 10), ("Recruitment", 10), ("Thaumaturgy", 0),
        ]),
        "subclasses": {
            "Balthazar's Bodyguard": {"effect": "+100% Attack.", "requiredSkillsExpert": ["Nightshade Magic", "Intelligence", "Leadership", "Diplomacy", "Offense"]},
            "Silvertongue's Envoy": {"effect": "+100% Defence.", "requiredSkillsExpert": ["Daylight Magic", "Scouting", "Luck", "Defence", "Sorcery"]},
        },
    },
    "Warlock": {
        "faction": "Dungeon",
        "type": "Magic",
        "factionSkill": "Triumvirate's Strength",
        "statGrowth": {"attack": {"base": 0, "1-12": 0.15, "13+": 0.25}, "defence": {"base": 2, "1-12": 0.2, "13+": 0.25}, "spellPower": {"base": 2, "1-12": 0.3, "13+": 0.25}, "knowledge": {"base": 3, "1-12": 0.35, "13+": 0.25}},
        "skillRollChances": skill_chances([
            ("Offense", 5), ("Defence", 5), ("Resistance", 5), ("Battlecraft", 5),
            ("Sorcery", 15), ("Intelligence", 15), ("Summon Avatar", 15), ("Battle Magic", 15),
            ("Daylight Magic", 5), ("Nightshade Magic", 5), ("Arcane Magic", 5), ("Primal Magic", 5),
            ("Leadership", 12.5), ("Luck", 7.5), ("Insight", 7.5), ("Diplomacy", 12.5),
            ("Logistics", 5), ("Scouting", 12.5), ("Economy", 12.5), ("Tactics", 10),
            ("Siegecraft", 10), ("Recruitment", 0), ("Thaumaturgy", 10),
        ]),
        "subclasses": {
            "Amelchia's Heir": {"effect": "+100% Spell Power.", "requiredSkillsExpert": ["Primal Magic", "Summon Avatar", "Battlecraft", "Insight", "Tactics"]},
            "Great Merchant": {"effect": "Grants +10,000 gold daily.", "requiredSkillsExpert": ["Arcane Magic", "Economy", "Battle Magic", "Logistics", "Resistance"]},
        },
    },
    "Warden": {
        "faction": "Grove",
        "type": "Might",
        "factionSkill": "Murmuring",
        "statGrowth": {"attack": {"base": 2, "1-12": 0.35, "13+": 0.25}, "defence": {"base": 1, "1-12": 0.35, "13+": 0.25}, "spellPower": {"base": 2, "1-12": 0.15, "13+": 0.25}, "knowledge": {"base": 2, "1-12": 0.15, "13+": 0.25}},
        "skillRollChances": skill_chances([("Murmuring", 100)]),
        "subclasses": {
            "Wellspring of Vigor": {"effect": "Generates maximum Focus Charges at the beginning of each round.", "requiredSkillsExpert": ["Battlecraft", "Intelligence", "Nightshade Magic", "Leadership", "Economy"]},
            "Fortune's Favored": {"effect": "Friendly creatures have maximum Luck and always land Lucky Strikes.", "requiredSkillsExpert": ["Daylight Magic", "Scouting", "Luck", "Defence", "Sorcery"]},
        },
        "note": "Grove heroes only roll Murmuring for secondary skills per wiki Warden page.",
    },
    "Druid": {
        "faction": "Grove",
        "type": "Magic",
        "factionSkill": "Murmuring",
        "statGrowth": {"attack": {"base": 1, "1-12": 0.15, "13+": 0.25}, "defence": {"base": 2, "1-12": 0.15, "13+": 0.25}, "spellPower": {"base": 2, "1-12": 0.35, "13+": 0.25}, "knowledge": {"base": 2, "1-12": 0.35, "13+": 0.25}},
        "skillRollChances": skill_chances([("Murmuring", 100)]),
        "subclasses": {
            "Celestial Envoy": {"effect": "The hero can use all spells.", "requiredSkillsExpert": ["Arcane Magic", "Battle Magic", "Defence", "Insight", "Scouting"]},
            "Heaven's Fury": {"effect": "Heroic Strike deals damage to all enemies in a 1-hex radius.", "requiredSkillsExpert": ["Primal Magic", "Economy", "Logistics", "Resistance", "Sorcery"]},
        },
        "note": "Grove heroes only roll Murmuring for secondary skills per wiki Druid page.",
    },
    "Enforcer": {
        "faction": "Hive",
        "type": "Might",
        "factionSkill": "Summon Swarm",
        "statGrowth": {"attack": {"base": 2, "1-12": 0.25, "13+": 0.25}, "defence": {"base": 2, "1-12": 0.25, "13+": 0.25}, "spellPower": {"base": 2, "1-12": 0.25, "13+": 0.25}, "knowledge": {"base": 1, "1-12": 0.25, "13+": 0.25}},
        "skillRollChances": skill_chances([
            ("Offense", 10), ("Defence", 10), ("Resistance", 10), ("Battlecraft", 10),
            ("Sorcery", 10), ("Intelligence", 10), ("Summon Avatar", 10), ("Battle Magic", 10),
            ("Daylight Magic", 10), ("Nightshade Magic", 10), ("Arcane Magic", 8), ("Primal Magic", 8),
            ("Leadership", 10), ("Luck", 10), ("Insight", 10), ("Diplomacy", 10),
            ("Logistics", 10), ("Scouting", 10), ("Economy", 10), ("Tactics", 10),
            ("Siegecraft", 10), ("Recruitment", 10), ("Thaumaturgy", 0),
        ]),
        "subclasses": {
            "Broodmother": {"effect": "Doubles the base stats of summoned Fire Larvae.", "requiredSkillsExpert": ["Battlecraft", "Intelligence", "Nightshade Magic", "Leadership", "Economy"]},
            "Soul Eater": {"effect": "Hero can consume a corpse for bonus Attack, Defence, and Spell Power until end of battle.", "requiredSkillsExpert": ["Daylight Magic", "Battle Magic", "Insight", "Logistics", "Resistance"]},
        },
    },
    "Herald": {
        "faction": "Hive",
        "type": "Magic",
        "factionSkill": "Summon Swarm",
        "statGrowth": {"attack": {"base": 1, "1-12": 0.25, "13+": 0.25}, "defence": {"base": 1, "1-12": 0.25, "13+": 0.25}, "spellPower": {"base": 3, "1-12": 0.25, "13+": 0.25}, "knowledge": {"base": 2, "1-12": 0.25, "13+": 0.25}},
        "skillRollChances": skill_chances([
            ("Offense", 10), ("Defence", 10), ("Resistance", 10), ("Battlecraft", 10),
            ("Sorcery", 10), ("Intelligence", 10), ("Summon Avatar", 10), ("Battle Magic", 10),
            ("Daylight Magic", 10), ("Nightshade Magic", 10), ("Arcane Magic", 8), ("Primal Magic", 8),
            ("Leadership", 10), ("Luck", 10), ("Insight", 10), ("Diplomacy", 10),
            ("Logistics", 10), ("Scouting", 10), ("Economy", 10), ("Tactics", 10),
            ("Siegecraft", 10), ("Recruitment", 0), ("Thaumaturgy", 10),
        ]),
        "subclasses": {
            "Progenitor": {"effect": "+200% creature growth in all your cities.", "requiredSkillsExpert": ["Defence", "Summon Avatar", "Arcane Magic", "Diplomacy", "Tactics"]},
            "Lord of Chaos": {"effect": "Heroic Strike deals +5 damage per hero attribute point.", "requiredSkillsExpert": ["Offense", "Sorcery", "Primal Magic", "Luck", "Scouting"]},
        },
    },
    "Oathkeeper": {
        "faction": "Schism",
        "type": "Might",
        "factionSkill": "Abyssal Communion",
        "statGrowth": {"attack": {"base": 3, "1-12": 0.25, "13+": 0.25}, "defence": {"base": 2, "1-12": 0.25, "13+": 0.25}, "spellPower": {"base": 1, "1-12": 0.25, "13+": 0.25}, "knowledge": {"base": 1, "1-12": 0.25, "13+": 0.25}},
        "skillRollChances": skill_chances([
            ("Offense", 10), ("Defence", 10), ("Resistance", 10), ("Battlecraft", 10),
            ("Sorcery", 10), ("Intelligence", 10), ("Summon Avatar", 10), ("Battle Magic", 10),
            ("Daylight Magic", 4), ("Nightshade Magic", 6), ("Arcane Magic", 8), ("Primal Magic", 2),
            ("Leadership", 10), ("Luck", 10), ("Insight", 7.5), ("Diplomacy", 5),
            ("Logistics", 15), ("Scouting", 12.5), ("Economy", 12.5), ("Tactics", 7.5),
            ("Siegecraft", 10), ("Recruitment", 10), ("Thaumaturgy", 0),
        ]),
        "subclasses": {
            "Unbound": {"effect": "Increases the level of all hero spells to their maximum.", "requiredSkillsExpert": ["Daylight Magic", "Scouting", "Offense", "Sorcery", "Leadership"]},
            "Unfeeling": {"effect": "Enemy loses all Focus Charges at the beginning of each battle round.", "requiredSkillsExpert": ["Nightshade Magic", "Resistance", "Diplomacy", "Intelligence", "Economy"]},
        },
    },
    "Riftspeaker": {
        "faction": "Schism",
        "type": "Magic",
        "factionSkill": "Abyssal Communion",
        "statGrowth": {"attack": {"base": 1, "1-12": 0.25, "13+": 0.25}, "defence": {"base": 1, "1-12": 0.25, "13+": 0.25}, "spellPower": {"base": 3, "1-12": 0.25, "13+": 0.25}, "knowledge": {"base": 2, "1-12": 0.25, "13+": 0.25}},
        "skillRollChances": skill_chances([
            ("Offense", 10), ("Defence", 10), ("Resistance", 10), ("Battlecraft", 10),
            ("Sorcery", 10), ("Intelligence", 10), ("Summon Avatar", 10), ("Battle Magic", 10),
            ("Daylight Magic", 4), ("Nightshade Magic", 6), ("Arcane Magic", 8), ("Primal Magic", 2),
            ("Leadership", 10), ("Luck", 10), ("Insight", 7.5), ("Diplomacy", 5),
            ("Logistics", 15), ("Scouting", 12.5), ("Economy", 12.5), ("Tactics", 7.5),
            ("Siegecraft", 10), ("Recruitment", 0), ("Thaumaturgy", 10),
        ]),
        "subclasses": {
            "Unstoppable": {"effect": "+10 Attack, Defence, Spell Power, and Knowledge.", "requiredSkillsExpert": ["Primal Magic", "Tactics", "Battle Magic", "Insight", "Battlecraft"]},
            "Unfathomable": {"effect": "All enemies always deal minimum and take maximum damage.", "requiredSkillsExpert": ["Arcane Magic", "Logistics", "Luck", "Summon Avatar", "Defence"]},
        },
    },
}

# Normalize Offense -> Offense (wiki uses Offence)
for h in heroes:
    for s in h["startingSkills"]:
        if s["skill"] == "Offence":
            s["skill"] = "Offense"
    if h.get("subclassAdvantage") == "Offence":
        h["subclassAdvantage"] = "Offense"

output = {"heroes": heroes, "classes": classes}
print(f"Hero count: {len(heroes)}")
for f in ["Temple", "Necropolis", "Dungeon", "Grove", "Hive", "Schism"]:
    print(f"  {f}: {sum(1 for x in heroes if x['faction']==f)}")

with open(r"b:\hmmOE\heroes_data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# Also print heroes array only for parent
with open(r"b:\hmmOE\heroes_array.json", "w", encoding="utf-8") as f:
    json.dump(heroes, f, ensure_ascii=False, indent=2)
