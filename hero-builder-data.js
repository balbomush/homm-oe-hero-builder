/* Heroes of Might and Magic: Olden Era — данные для конструктора героя */
window.HOE_BUILDER_DATA = {
  factions: {
    Temple: { skill: "Righteousness", color: "#c9a227" },
    Necropolis: { skill: "Necromancy", color: "#7b6ba8" },
    Grove: { skill: "Murmuring", color: "#3d8b5a" },
    Dungeon: { skill: "Triumvirate's Strength", color: "#8b3a62" },
    Hive: { skill: "Summon Swarm", color: "#c45c26" },
    Schism: { skill: "Abyssal Communion", color: "#4a6fa5" }
  },

  skillAliases: {
    Offence: "Offense",
    Intelligence: "Wisdom",
    Ascension: "Righteousness",
    "Call Swarm": "Summon Swarm"
  },

  skills: {
    Offense: { cat: "might", might: true, adv: ["Archery", "Battle March", "Battle Frenzy"], exp: ["Shadow Blades", "Reality Wardens", "Firmness"] },
    Defence: { cat: "might", might: true, adv: ["Cover", "Hymn to the Martyrs", "As Luck Would Have It"], exp: ["Shields and Shells", "Wizard Contract", "Unstoppable Force"] },
    Battlecraft: { cat: "might", might: true, adv: ["Melee Mastery", "Ranged Mastery", "Overwatch"], exp: ["Battle Focus", "Preemptive Strike", "Manacraft"] },
    Leadership: { cat: "might", might: true, adv: ["Resolve", "Where the Sun Never Sets", "Hero of Legends"], exp: ["Inspiring Strike", "March!", "Enthusiasm"] },
    Luck: { cat: "might", might: true, adv: ["Beastly Confidence", "Always Heads", "Mearea's Chosen"], exp: ["Lucky Hit", "Lightning Strikes Twice", "Lucky Day"] },
    Resistance: { cat: "might", might: true, adv: ["Obstruction", "Hindrance Aura", "Fast Metabolism"], exp: ["Magic Suppression", "Time Shift", "Draining"] },
    Siegecraft: { cat: "might", might: true, adv: ["Relentless Assault", "Forward Observers", "Barrage"], exp: ["Phalanx", "Tunnelling", "Sabotage"] },
    Tactics: { cat: "might", might: true, adv: ["One for All", "Easy Prey", "Energizing Mana"], exp: ["All for One", "Riposte Mastery", "Spellcaster Tactics"] },
    Recruitment: { cat: "might", might: true, magic: false, adv: ["Direct Supervision", "Elite Guards", "Veterans"], exp: ["Relocation", "Strenuous Training", "Mentors"] },
    Combat: { cat: "might", might: true, magic: false, adv: ["Effortless Strike", "Revenge", "Mighty Strike"], exp: ["Swordcraft", "Battle Thrill", "Confusing Strike"] },
    Wisdom: { cat: "magic", magic: true, adv: ["Rite of Magic", "Between the Lines", "Seeing Through"], exp: ["Rhythmic Cadence", "Eagle Eye", "Stargazer"] },
    "Battle Magic": { cat: "magic", magic: true, adv: ["Aura of Destruction", "Aura of Protection", "Aura of Wizardry"], exp: ["Battle Mage's Authority", "Mage Protector's Authority", "Magic Time"] },
    Sorcery: { cat: "magic", magic: true, adv: ["Magical Influence", "Magic Arrow", "Raw Energy"], exp: ["Piercing Spells", "High Mage", "Sticky Magic"] },
    Thaumaturgy: { cat: "magic", magic: true, might: false, adv: ["Antimage", "Ancient Scrolls", "Practical Incantations"], exp: ["Thaumaturge Brilliance", "Vast Soul", "Archmage"] },
    "Summon Avatar": { cat: "magic", magic: true, adv: ["Avatar of Fury", "Avatar of Toughness", "Avatar of Celerity"], exp: ["Stabilization", "Their Name is Legion", "Fields of Mana"] },
    "Daylight Magic": { cat: "magic", magic: true, adv: ["Daylight Time", "Luminous Focus", "Brightest Sun"], exp: ["Daylight Teachings", "Speed of Light", "Scholar Synergy: Arina"] },
    "Nightshade Magic": { cat: "magic", magic: true, adv: ["Nightshade Time", "Chronic Weakness", "Darkest Night"], exp: ["Nightshade Teachings", "Hour of the Wolf", "Scholar Synergy: Naira"] },
    "Arcane Magic": { cat: "magic", magic: true, adv: ["Arcane Time", "All Life is Endless", "Purest Thought"], exp: ["Arcane Teachings", "Mana Flex", "Scholar Synergy: Doreath"] },
    "Primal Magic": { cat: "magic", magic: true, adv: ["Primal Time", "Primal Force", "Sharpest Teeth"], exp: ["Primal Teachings", "Chaos Reigns", "Scholar Synergy: Hksmilla"] },
    Logistics: { cat: "general", adv: ["Leaps and Bounds", "Strong Mounts", "Careful Planning"], exp: ["Secret Passages", "Back to Town!", "Battle Logistics"] },
    Scouting: { cat: "general", adv: ["Long-Sight", "Familiar Paths", "Pathfinding"], exp: ["Reconnaissance", "Visions", "Counterespionage"] },
    Diplomacy: { cat: "general", adv: ["Larger Than Life", "Eloquence", "Folk Hero"], exp: ["Art of the Deal", "Vagrant Army", "Negotiator"] },
    Economy: { cat: "general", adv: ["Tax Collector", "Smuggler", "Master Builder"], exp: ["Experimenter", "Merchant", "Antiquarian"] },
    Insight: { cat: "general", adv: ["Enlightenment", "Civic Innovation", "Sagacity"], exp: ["Scholar of Magic", "Endless Charisma", "Perception"] },
    Righteousness: { cat: "faction", faction: true, adv: ["Fields of Serenity", "Righteous Sacrifice", "Purging Touch"], exp: ["Guardian", "The Chosen One", "Strong Faith"] },
    Necromancy: { cat: "faction", faction: true, adv: ["Gravesoil", "Soul Harvest", "Death Herald"], exp: ["Soul Reaper", "Eternal Service", "Fields of the Dead"] },
    "Summon Swarm": { cat: "faction", faction: true, adv: ["Warmth of the Nest", "Thy Children", "Ravage"], exp: ["Hive Power", "Hardened Shells", "Hive Flame"] },
    Murmuring: { cat: "faction", faction: true, adv: ["Mycelium Grounds", "Life Essence", "Child of the Woods"], exp: ["Just One More Time", "Burst of Energy", "Strong Connection"] },
    "Triumvirate's Strength": { cat: "faction", faction: true, adv: ["Underground Passages", "Alvarian Expertise", "Underground Mana Pools"], exp: ["Jack of All Trades", "Flow", "Opportunists"] },
    "Abyssal Communion": { cat: "faction", faction: true, adv: ["Our True Home", "Comprehensible Depths", "Call of the Void"], exp: ["Black Ice", "Abyssopelagial", "Celestial Abyss"] }
  },

  classes: {
    Knight: {
      faction: "Temple", type: "Might", skillChances: {
        Offense: 15, Defence: 15, Resistance: 15, Battlecraft: 15, Sorcery: 5, Wisdom: 5,
        "Summon Avatar": 5, "Battle Magic": 5, "Daylight Magic": 8, "Nightshade Magic": 2,
        "Arcane Magic": 6, "Primal Magic": 4, Leadership: 15, Luck: 5, Insight: 10,
        Diplomacy: 10, Logistics: 10, Scouting: 10, Economy: 10, Tactics: 10, Siegecraft: 10, Recruitment: 10
      },
      subclasses: {
        Swashbuckler: { bonus: "Heroic Strike +200 base Damage", bonusEn: "Heroic Strike +200 base Damage", bonusRu: "Героический удар +200 базового урона", skills: ["Nightshade Magic", "Wisdom", "Leadership", "Luck", "Offense"] },
        Paragon: { bonus: "Союзники: max/min урон", bonusEn: "Allies deal max/min damage", bonusRu: "Союзники наносят макс./мин. урон", skills: ["Daylight Magic", "Battlecraft", "Tactics", "Diplomacy", "Summon Avatar"] }
      }
    },
    Cleric: {
      faction: "Temple", type: "Magic", skillChances: {
        Offense: 5, Defence: 5, Resistance: 5, Battlecraft: 5, Sorcery: 15, Wisdom: 15,
        "Summon Avatar": 15, "Battle Magic": 15, "Daylight Magic": 8, "Nightshade Magic": 2,
        "Arcane Magic": 6, "Primal Magic": 4, Leadership: 15, Luck: 5, Insight: 10,
        Diplomacy: 10, Logistics: 10, Scouting: 10, Economy: 10, Tactics: 10, Siegecraft: 10, Thaumaturgy: 10
      },
      subclasses: {
        "Grand Inquisitor": { bonus: "Враг: 1 каст/заклинание", bonusEn: "Enemies: 1 cast per spell", bonusRu: "Враг: 1 каст/заклинание", skills: ["Arcane Magic", "Battle Magic", "Defence", "Insight", "Scouting"] },
        Ascendant: { bonus: "Все заклинания 0 маны", bonusEn: "All spells cost 0 mana", bonusRu: "Все заклинания 0 маны", skills: ["Primal Magic", "Economy", "Logistics", "Resistance", "Sorcery"] }
      }
    },
    "Death Knight": {
      faction: "Necropolis", type: "Might", skillChances: {
        Offense: 15, Defence: 15, Resistance: 15, Battlecraft: 15, Sorcery: 5, Wisdom: 5,
        "Summon Avatar": 5, "Battle Magic": 5, "Daylight Magic": 2, "Nightshade Magic": 8,
        "Arcane Magic": 6, "Primal Magic": 4, Leadership: 0, Luck: 15, Insight: 15,
        Diplomacy: 7.5, Logistics: 10, Scouting: 10, Economy: 10, Tactics: 7.5, Siegecraft: 10, Recruitment: 10
      },
      subclasses: {
        "Harbinger of Doom": { bonus: "Min Luck врага, doom strikes", bonusEn: "Min enemy Luck, doom strikes", bonusRu: "Мин. удача врага, удары рока", skills: ["Defence", "Luck", "Primal Magic", "Scouting", "Sorcery"] },
        "Walking Rot": { bonus: "Min Morale врага", bonusEn: "Min enemy Morale", bonusRu: "Мин. мораль врага", skills: ["Resistance", "Tactics", "Diplomacy", "Nightshade Magic", "Wisdom"] }
      }
    },
    Necromancer: {
      faction: "Necropolis", type: "Magic", skillChances: {
        Offense: 5, Defence: 5, Resistance: 5, Battlecraft: 5, Sorcery: 15, Wisdom: 15,
        "Summon Avatar": 15, "Battle Magic": 15, "Daylight Magic": 2, "Nightshade Magic": 8,
        "Arcane Magic": 6, "Primal Magic": 4, Leadership: 0, Luck: 15, Insight: 15,
        Diplomacy: 7.5, Logistics: 10, Scouting: 10, Economy: 10, Tactics: 7.5, Siegecraft: 10, Thaumaturgy: 10
      },
      subclasses: {
        Soulweaver: { bonus: "Wights на месте трупов", bonusEn: "Wights spawn from corpses", bonusRu: "Врайты появляются на месте трупов", skills: ["Summon Avatar", "Arcane Magic", "Battlecraft", "Insight", "Logistics"] },
        Chronomancer: { bonus: "Necromancy для всех типов", bonusEn: "Necromancy for all unit types", bonusRu: "Некромантия для всех типов существ", skills: ["Daylight Magic", "Tactics", "Battle Magic", "Offense", "Economy"] }
      }
    },
    Warden: {
      faction: "Grove", type: "Might", skillChances: {},
      subclasses: {
        "Fortune's Favored": { bonus: "Max Luck + всегда Lucky Strike", bonusEn: "Max Luck + always Lucky Strike", bonusRu: "Макс. удача + всегда удачный удар", skills: ["Diplomacy", "Wisdom", "Luck", "Offense", "Primal Magic"] },
        "Wellspring of Vigor": { bonus: "Max Focus Charges каждый раунд", bonusEn: "Max Focus Charges every round", bonusRu: "Макс. заряды фокуса каждый раунд", skills: ["Arcane Magic", "Battle Magic", "Defence", "Insight", "Scouting"] }
      }
    },
    Druid: {
      faction: "Grove", type: "Magic", skillChances: {},
      subclasses: {
        "Celestial Envoy": { bonus: "Все школы заклинаний", bonusEn: "All magic schools", bonusRu: "Все школы заклинаний", skills: ["Defence", "Summon Avatar", "Arcane Magic", "Scouting", "Economy"] },
        "Heaven's Fury": { bonus: "Heroic Strike AoE 1 hex", bonusEn: "Heroic Strike AoE 1 hex", bonusRu: "Героический удар: AoE 1 гекс", skills: ["Battlecraft", "Sorcery", "Nightshade Magic", "Logistics", "Tactics"] }
      }
    },
    Overlord: {
      faction: "Dungeon", type: "Might", skillChances: {
        Offense: 15, Defence: 15, Resistance: 15, Battlecraft: 15, Sorcery: 5, Wisdom: 5,
        "Summon Avatar": 5, "Battle Magic": 5, "Daylight Magic": 5, "Nightshade Magic": 5,
        "Arcane Magic": 5, "Primal Magic": 5, Leadership: 12.5, Luck: 7.5, Insight: 7.5,
        Diplomacy: 12.5, Logistics: 5, Scouting: 12.5, Economy: 12.5, Tactics: 10, Siegecraft: 10, Recruitment: 10
      },
      subclasses: {
        "Balthazar's Bodyguard": { bonus: "+100% Attack", bonusEn: "+100% Attack", bonusRu: "+100% атаки", skills: ["Offense", "Nightshade Magic", "Leadership", "Diplomacy", "Wisdom"] },
        "Silvertongue's Envoy": { bonus: "+100% Defence", bonusEn: "+100% Defence", bonusRu: "+100% защиты", skills: ["Defence", "Daylight Magic", "Luck", "Sorcery", "Scouting"] }
      }
    },
    Warlock: {
      faction: "Dungeon", type: "Magic", skillChances: {
        Offense: 5, Defence: 5, Resistance: 5, Battlecraft: 5, Sorcery: 15, Wisdom: 15,
        "Summon Avatar": 15, "Battle Magic": 15, "Daylight Magic": 5, "Nightshade Magic": 5,
        "Arcane Magic": 5, "Primal Magic": 5, Leadership: 12.5, Luck: 7.5, Insight: 7.5,
        Diplomacy: 12.5, Logistics: 5, Scouting: 12.5, Economy: 12.5, Tactics: 10, Siegecraft: 10, Thaumaturgy: 10
      },
      subclasses: {
        "Amelchia's Heir": { bonus: "+100% Spell Power", bonusEn: "+100% Spell Power", bonusRu: "+100% силы заклинаний", skills: ["Primal Magic", "Summon Avatar", "Insight", "Battlecraft", "Tactics"] },
        "Great Merchant": { bonus: "+10 000 золота/день", bonusEn: "+10,000 gold/day", bonusRu: "+10 000 золота/день", skills: ["Arcane Magic", "Resistance", "Battle Magic", "Economy", "Logistics"] }
      }
    },
    Enforcer: {
      faction: "Hive", type: "Might", skillChances: {},
      subclasses: {
        Broodmother: { bonus: "×2 статы Fire Larvae", bonusEn: "×2 Fire Larvae base stats", bonusRu: "×2 статы Fire Larvae", skills: ["Nightshade Magic", "Battlecraft", "Economy", "Wisdom", "Leadership"] },
        "Soul Eater": { bonus: "Поедание трупов → статы", bonusEn: "Corpse eating → stacking stats", bonusRu: "Поедание трупов → статы", skills: ["Daylight Magic", "Battle Magic", "Insight", "Logistics", "Resistance"] }
      }
    },
    Herald: {
      faction: "Hive", type: "Magic", skillChances: {},
      subclasses: {
        Progenitor: { bonus: "+200% рост существ", bonusEn: "+200% creature growth", bonusRu: "+200% рост существ", skills: ["Insight", "Defence", "Diplomacy", "Summon Avatar", "Tactics"] },
        "Lord of Chaos": { bonus: "Heroic Strike +5 за stat point", bonusEn: "Heroic Strike +5 per stat point", bonusRu: "Героический удар +5 за пункт характеристики", skills: ["Primal Magic", "Luck", "Offense", "Scouting", "Sorcery"] }
      }
    },
    Oathkeeper: {
      faction: "Schism", type: "Might", skillChances: {
        Offense: 10, Defence: 10, Resistance: 10, Battlecraft: 10, Sorcery: 10, Wisdom: 10,
        "Summon Avatar": 10, "Battle Magic": 10, "Daylight Magic": 4, "Nightshade Magic": 6,
        "Arcane Magic": 8, "Primal Magic": 2, Leadership: 10, Luck: 10, Insight: 7.5,
        Diplomacy: 5, Logistics: 15, Scouting: 12.5, Economy: 12.5, Tactics: 7.5, Siegecraft: 10, Recruitment: 10
      },
      subclasses: {
        Unbound: { bonus: "Max уровень всех заклинаний", bonusEn: "Max level for all spells", bonusRu: "Макс. уровень всех заклинаний", skills: ["Daylight Magic", "Scouting", "Offense", "Sorcery", "Leadership"] },
        Unfeeling: { bonus: "Враг теряет весь Focus/раунд", bonusEn: "Enemies lose all Focus/round", bonusRu: "Враг теряет весь фокус за раунд", skills: ["Nightshade Magic", "Resistance", "Diplomacy", "Wisdom", "Economy"] }
      }
    },
    Riftspeaker: {
      faction: "Schism", type: "Magic", skillChances: {},
      subclasses: {
        Unstoppable: { bonus: "+10 ко всем статам", bonusEn: "+10 to all stats", bonusRu: "+10 ко всем статам", skills: ["Battle Magic", "Insight", "Battlecraft", "Tactics", "Primal Magic"] },
        Unfathomable: { bonus: "Враги: min/max урон", bonusEn: "Enemies deal min/max damage", bonusRu: "Враги наносят макс./мин. урон", skills: ["Arcane Magic", "Logistics", "Luck", "Summon Avatar", "Defence"] }
      }
    }
  },

};
