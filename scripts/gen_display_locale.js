#!/usr/bin/env node
/** Generates hero-builder-display-locale.js from wiki_ru_official.json + fallbacks */
const fs = require("fs");
const path = require("path");
const root = path.join(__dirname, "..");

const dataSrc = fs.readFileSync(path.join(root, "hero-builder-data.js"), "utf8");
const skillsMatch = dataSrc.match(/skills:\s*\{([\s\S]*?)\n\s*\},\s*\n\s*classes:/);
const classesMatch = dataSrc.match(/classes:\s*\{([\s\S]*?)\n\s*\},\s*\n\s*\};/);
if (!skillsMatch || !classesMatch) {
  console.error("Failed to parse hero-builder-data.js");
  process.exit(1);
}
const skills = eval("({" + skillsMatch[1] + "})");
const classes = eval("({" + classesMatch[1] + "})");

const wiki = JSON.parse(fs.readFileSync(path.join(root, "scripts/wiki_ru_official.json"), "utf8"));

// Fallback RU for keys missing on wiki (no RU page or broken template)
const fallbackRu = {
  skills: {
    "Summon Swarm": "Призыв роя",
    Murmuring: "Шёпот леса",
  },
  subskills: {
    "Warmth of the Nest": "Тепло гнезда",
    "Thy Children": "Твои дети",
    Ravage: "Опустошение",
    "Hive Power": "Сила улья",
    "Hardened Shells": "Закалённые панцири",
    "Hive Flame": "Пламя улья",
    "Mycelium Grounds": "Грибница",
    "Life Essence": "Сущность жизни",
    "Child of the Woods": "Дитя леса",
    "Just One More Time": "Ещё один раз",
    "Burst of Energy": "Всплеск энергии",
    "Strong Connection": "Сильная связь",
    "Scholar Synergy: Naira": "Синергия магов. Наира",
    "Scholar Synergy: Hksmilla": "Синергия магов. Кшмилья",
    "Battle Logistics": "Боевая логистика",
    Negotiator: "Переговорщик",
    Antiquarian: "Антиквар",
    Perception: "Восприятие",
    "Strong Faith": "Твёрдая вера",
    "Fields of the Dead": "Поля мёртвых",
    Counterespionage: "Контрразведка",
    Opportunists: "Оппортунисты",
    "Celestial Abyss": "Небесная бездна",
    Experimenter: "Экспериментатор",
  },
  subclasses: {
    Swashbuckler: "Авантюрист",
    Paragon: "Парангон",
    "Grand Inquisitor": "Великий инквизитор",
    Ascendant: "Вознесённый",
    "Harbinger of Doom": "Предвестник гибели",
    "Walking Rot": "Гниющая хода",
    Soulweaver: "Ткач душ",
    Chronomancer: "Хрономант",
    "Fortune's Favored": "Любимец фортуны",
    "Wellspring of Vigor": "Источник бодрости",
    "Celestial Envoy": "Небесный посланник",
    "Heaven's Fury": "Ярость небес",
    "Balthazar's Bodyguard": "Телохранитель Балтазара",
    "Silvertongue's Envoy": "Посланник Серебряного языка",
    "Amelchia's Heir": "Наследник Амельчии",
    "Great Merchant": "Великий купец",
    Broodmother: "Матка роя",
    "Soul Eater": "Пожиратель душ",
    Progenitor: "Прародитель",
    "Lord of Chaos": "Повелитель хаоса",
    Unbound: "Неукротимый",
    Unfeeling: "Бесчувственный",
    Unstoppable: "Неостановимый",
    Unfathomable: "Непостижимый",
  },
};

const skillKeys = Object.keys(skills);
const subKeys = new Set();
skillKeys.forEach((k) => {
  (skills[k].adv || []).forEach((x) => subKeys.add(x));
  (skills[k].exp || []).forEach((x) => subKeys.add(x));
});
const subclassKeys = new Set();
Object.values(classes).forEach((c) => {
  Object.keys(c.subclasses || {}).forEach((k) => subclassKeys.add(k));
});

function pick(map, key, fallbacks) {
  const v = map[key];
  if (v && v !== key) return v;
  if (fallbacks[key]) return fallbacks[key];
  return key;
}

const skillRu = {};
skillKeys.forEach((k) => {
  skillRu[k] = pick(wiki.skills, k, fallbackRu.skills);
});

const subRu = {};
[...subKeys].forEach((k) => {
  subRu[k] = pick(wiki.subskills, k, fallbackRu.subskills);
});

const subclassRu = {};
[...subclassKeys].forEach((k) => {
  subclassRu[k] = pick(wiki.subclasses || {}, k, fallbackRu.subclasses);
});

const missingSubs = [...subKeys].filter((k) => subRu[k] === k);
if (missingSubs.length) {
  console.error("Missing RU subskill translations:", missingSubs);
  process.exit(1);
}

const missingSkills = skillKeys.filter((k) => skillRu[k] === k);
if (missingSkills.length) {
  console.error("Missing RU skill translations:", missingSkills);
  process.exit(1);
}

function identity(keys) {
  const o = {};
  keys.forEach((k) => { o[k] = k; });
  return o;
}

const skillEn = identity(skillKeys);
const subEn = identity([...subKeys]);
const subclassEn = identity([...subclassKeys]);

const out = `/* HoMM OE Hero Builder — display names for skills / subskills / subclasses (generated) */
/* RU names: official Hooded Horse wiki (scripts/wiki_ru_official.json) + fallbacks */
window.HOE_BUILDER_DISPLAY = {
  skills: {
    en: ${JSON.stringify(skillEn, null, 2)},
    ru: ${JSON.stringify(skillRu, null, 2)}
  },
  subskills: {
    en: ${JSON.stringify(subEn, null, 2)},
    ru: ${JSON.stringify(subRu, null, 2)}
  },
  subclasses: {
    en: ${JSON.stringify(subclassEn, null, 2)},
    ru: ${JSON.stringify(subclassRu, null, 2)}
  },
  skill(lang, key) {
    const m = this.skills[lang] || this.skills.en;
    return (m && m[key]) || key;
  },
  subskill(lang, key) {
    if (!key) return "";
    const m = this.subskills[lang] || this.subskills.en;
    return (m && m[key]) || key;
  },
  subclass(lang, key) {
    const m = this.subclasses[lang] || this.subclasses.en;
    return (m && m[key]) || key;
  }
};
`;

fs.writeFileSync(path.join(root, "hero-builder-display-locale.js"), out, "utf8");
console.log("Wrote hero-builder-display-locale.js");
console.log("Skills:", skillKeys.length, "Subskills:", subKeys.size, "Subclasses:", subclassKeys.size);
