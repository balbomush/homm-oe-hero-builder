#!/usr/bin/env node
/** Generates hero-builder-display-locale.js — RU display names for skills, subskills, subclasses */
const fs = require("fs");
const path = require("path");
const root = path.join(__dirname, "..");
const dataSrc = fs.readFileSync(path.join(root, "hero-builder-data.js"), "utf8");
const skills = eval("({" + dataSrc.match(/skills:\s*\{([\s\S]*?)\n  \},\n\n  classes/)[1] + "})");
const classes = eval("({" + dataSrc.match(/classes:\s*\{([\s\S]*?)\n  \},\n\n\};/)[1] + "})");

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

const skillRu = {
  Offense: "Нападение",
  Defence: "Защита",
  Battlecraft: "Боевое мастерство",
  Leadership: "Лидерство",
  Luck: "Удача",
  Resistance: "Сопротивление",
  Siegecraft: "Осада",
  Tactics: "Тактика",
  Recruitment: "Вербовка",
  Combat: "Боевые искусства",
  Wisdom: "Мудрость",
  "Battle Magic": "Боевая магия",
  Sorcery: "Колдовство",
  Thaumaturgy: "Тауматургия",
  "Summon Avatar": "Призыв аватара",
  "Daylight Magic": "Магия дня",
  "Nightshade Magic": "Магия ночной тени",
  "Arcane Magic": "Магия тайн",
  "Primal Magic": "Первобытная магия",
  Logistics: "Логистика",
  Scouting: "Разведка",
  Diplomacy: "Дипломатия",
  Economy: "Экономика",
  Insight: "Проницательность",
  Righteousness: "Праведность",
  Necromancy: "Некромантия",
  "Summon Swarm": "Призыв роя",
  Murmuring: "Шёпот леса",
  "Triumvirate's Strength": "Сила триумвирата",
  "Abyssal Communion": "Бездонное общение",
};

const subclassRu = {
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
};

const subRu = {
  Archery: "Стрельба",
  "Battle March": "Боевой марш",
  "Battle Frenzy": "Боевой раж",
  "Shadow Blades": "Теневые клинки",
  "Reality Wardens": "Стражи реальности",
  Firmness: "Твёрдость",
  Cover: "Укрытие",
  "Hymn to the Martyrs": "Гимн мученикам",
  "As Luck Would Have It": "Как повезёт",
  "Shields and Shells": "Щиты и панцири",
  "Wizard Contract": "Договор с магом",
  "Unstoppable Force": "Неудержимая сила",
  "Melee Mastery": "Мастерство ближнего боя",
  "Ranged Mastery": "Мастерство дальнего боя",
  Overwatch: "Караульная стража",
  "Battle Focus": "Боевой фокус",
  "Preemptive Strike": "Опережающий удар",
  Manacraft: "Мастерство маны",
  Resolve: "Решимость",
  "Where the Sun Never Sets": "Где солнце не садится",
  "Hero of Legends": "Герой легенд",
  "Inspiring Strike": "Воодушевляющий удар",
  "March!": "Марш!",
  Enthusiasm: "Энтузиазм",
  "Beastly Confidence": "Звериная уверенность",
  "Always Heads": "Всегда орёл",
  "Mearea's Chosen": "Избранник Меареи",
  "Lucky Hit": "Удачный удар",
  "Lightning Strikes Twice": "Молния бьёт дважды",
  "Lucky Day": "Удачный день",
  Obstruction: "Препятствие",
  "Hindrance Aura": "Аура помех",
  "Fast Metabolism": "Быстрый метаболизм",
  "Magic Suppression": "Подавление магии",
  "Time Shift": "Сдвиг времени",
  Draining: "Истощение",
  "Relentless Assault": "Неумолимая атака",
  "Forward Observers": "Передовые наблюдатели",
  Barrage: "Заградительный огонь",
  Phalanx: "Фаланга",
  Tunnelling: "Туннелирование",
  Sabotage: "Саботаж",
  "One for All": "Один за всех",
  "Easy Prey": "Лёгкая добыча",
  "Energizing Mana": "Заряжающая мана",
  "All for One": "Все за одного",
  "Riposte Mastery": "Мастерство контратаки",
  "Spellcaster Tactics": "Тактика заклинателя",
  "Direct Supervision": "Прямой надзор",
  "Elite Guards": "Элитная охрана",
  Veterans: "Ветераны",
  Relocation: "Перебазирование",
  "Strenuous Training": "Усиленная тренировка",
  Mentors: "Наставники",
  "Effortless Strike": "Лёгкий удар",
  Revenge: "Месть",
  "Mighty Strike": "Мощный удар",
  Swordcraft: "Мастерство меча",
  "Battle Thrill": "Боевой азарт",
  "Confusing Strike": "Сбивающий удар",
  "Rite of Magic": "Обряд магии",
  "Between the Lines": "Между строк",
  "Seeing Through": "Проницательный взгляд",
  "Rhythmic Cadence": "Ритмичный каденс",
  "Eagle Eye": "Орлиный глаз",
  Stargazer: "Звездочёт",
  "Aura of Destruction": "Аура разрушения",
  "Aura of Protection": "Аура защиты",
  "Aura of Wizardry": "Аура колдовства",
  "Battle Mage's Authority": "Власть боевого мага",
  "Mage Protector's Authority": "Власть защитника-мага",
  "Magic Time": "Магическое время",
  "Magical Influence": "Магическое влияние",
  "Magic Arrow": "Магическая стрела",
  "Raw Energy": "Чистая энергия",
  "Piercing Spells": "Пронзающие заклинания",
  "High Mage": "Верховный маг",
  "Sticky Magic": "Липкая магия",
  Antimage: "Антимаг",
  "Ancient Scrolls": "Древние свитки",
  "Practical Incantations": "Практические заклинания",
  "Thaumaturge Brilliance": "Блеск тауматурга",
  "Vast Soul": "Обширная душа",
  Archmage: "Архимаг",
  "Avatar of Fury": "Аватар ярости",
  "Avatar of Toughness": "Аватар стойкости",
  "Avatar of Celerity": "Аватар проворства",
  "Legion From Legion": "Легион из легиона",
  Stabilization: "Стабилизация",
  "Daylight Time": "Время дня",
  "Luminous Focus": "Светлый фокус",
  "Brightest Sun": "Ярчайшее солнце",
  "Daylight Teachings": "Учения дня",
  "Speed of Light": "Скорость света",
  "Scholar Synergy: Arina": "Синергия учёных: Арина",
  "Nightshade Time": "Время ночной тени",
  "Chronic Weakness": "Хроническая слабость",
  "Darkest Night": "Самая тёмная ночь",
  "Nightshade Teachings": "Учения ночной тени",
  "Hour of the Wolf": "Час волка",
  "Scholar Synergy: Naira": "Синергия учёных: Найра",
  "Arcane Time": "Время тайн",
  "All Life is Endless": "Вся жизнь бесконечна",
  "Purest Thought": "Чистейшая мысль",
  "Arcane Teachings": "Учения тайн",
  "Mana Flex": "Гибкая мана",
  "Scholar Synergy: Doreath": "Синергия учёных: Дореат",
  "Primal Time": "Первобытное время",
  "Primal Force": "Первобытная сила",
  "Sharpest Teeth": "Острейшие клыки",
  "Primal Teachings": "Первобытные учения",
  "Chaos Reigns": "Царствует хаос",
  "Scholar Synergy: Hksmilla": "Синергия учёных: Хксмилла",
  "Leaps and Bounds": "Скачками",
  "Strong Mounts": "Крепкие скакуны",
  "Careful Planning": "Тщательное планирование",
  "Secret Passages": "Тайные проходы",
  "Back to Town!": "Назад в город!",
  "Battle Logistics": "Боевая логистика",
  "Long-Sight": "Дальний обзор",
  "Familiar Paths": "Знакомые тропы",
  Pathfinding: "Следопытство",
  Reconnaissance: "Разведка",
  Visions: "Видения",
  Counterespionage: "Контрразведка",
  "Larger Than Life": "Больше, чем кажется",
  Eloquence: "Красноречие",
  "Folk Hero": "Народный герой",
  "Art of the Deal": "Искусство сделки",
  "Vagrant Army": "Армия бродяг",
  Negotiator: "Переговорщик",
  "Tax Collector": "Сборщик налогов",
  Smuggler: "Контрабандист",
  "Master Builder": "Мастер-строитель",
  Experimenter: "Экспериментатор",
  Merchant: "Торговец",
  Antiquarian: "Антиквар",
  Enlightenment: "Просвещение",
  "Civic Innovation": "Гражданские инновации",
  Sagacity: "Мудрость",
  "Scholar of Magic": "Учёный магии",
  "Endless Charisma": "Бесконечная харизма",
  Perception: "Восприятие",
  "Fields of Serenity": "Поля безмятежности",
  "Righteous Sacrifice": "Праведная жертва",
  "Purging Touch": "Очищающее касание",
  Guardian: "Страж",
  "The Chosen One": "Избранный",
  "Strong Faith": "Твёрдая вера",
  Gravesoil: "Почва могил",
  "Soul Harvest": "Сбор душ",
  "Death Herald": "Вестник смерти",
  "Soul Reaper": "Жнец душ",
  "Eternal Service": "Вечная служба",
  "Fields of the Dead": "Поля мёртвых",
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
  "Underground Passages": "Подземные ходы",
  "Alvarian Expertise": "Экспертиза алварцев",
  "Underground Mana Pools": "Подземные мана-источники",
  "Jack of All Trades": "Мастер на все руки",
  Flow: "Поток",
  Opportunists: "Оппортунисты",
  "Our True Home": "Наш истинный дом",
  "Comprehensible Depths": "Постижимые глубины",
  "Call of the Void": "Зов пустоты",
  "Black Ice": "Чёрный лёд",
  Abyssopelagial: "Бездонные глубины",
  "Celestial Abyss": "Небесная бездна",
};

function identity(keys) {
  const o = {};
  keys.forEach((k) => { o[k] = k; });
  return o;
}

const skillEn = identity(skillKeys);
const subEn = identity([...subKeys]);
const subclassEn = identity([...subclassKeys]);

skillKeys.forEach((k) => { if (!skillRu[k]) skillRu[k] = k; });
[...subKeys].forEach((k) => { if (!subRu[k]) subRu[k] = k; });
[...subclassKeys].forEach((k) => { if (!subclassRu[k]) subclassRu[k] = k; });

const missingSubs = [...subKeys].filter((k) => subRu[k] === k);
if (missingSubs.length) {
  console.error("Missing RU subskill translations:", missingSubs);
  process.exit(1);
}

const out = `/* HoMM OE Hero Builder — display names for skills / subskills / subclasses (generated) */
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
