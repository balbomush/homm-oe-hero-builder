const DATA = window.HOE_BUILDER_DATA;
const SYN = window.HOE_BUILDER_SYNERGIES || [];
const I18N = window.HOE_BUILDER_I18N;
const TIERS = ["", "Basic", "Advanced", "Expert"];
const SLOT_COUNT = 8;
let lang = localStorage.getItem("hoe_builder_lang") || "ru";
let state = {
  faction: "Temple",
  heroId: null,
  selectedSlot: null,
  targetSubclass: null,
  slots: Array(SLOT_COUNT).fill(null)
};
let levelPlan = {};
let levelOffers = {};

function t(key, vars) {
  let s = (I18N[lang] && I18N[lang][key]) || I18N.en[key] || key;
  if (vars) Object.entries(vars).forEach(([k, v]) => { s = s.replace("{" + k + "}", v); });
  return s;
}

function tierLabel(tier) {
  if (tier === 1) return t("tierBasic");
  if (tier === 2) return t("tierAdvanced");
  if (tier === 3) return t("tierExpert");
  return t("empty");
}

function heroDesc(hero) {
  if (!hero) return "";
  return lang === "ru"
    ? (hero.specialtyDescRu || hero.specialtyDescEn || "")
    : (hero.specialtyDescEn || hero.specialtyDescRu || "");
}

function subclassBonus(data) {
  return lang === "ru" ? (data.bonusRu || data.bonus || data.bonusEn) : (data.bonusEn || data.bonus || data.bonusRu);
}

function factionLabel(f) {
  return (I18N[lang].factions && I18N[lang].factions[f]) || f;
}

function normSkill(name) {
  return DATA.skillAliases[name] || name;
}

function getHero() {
  return DATA.heroes.find(h => h.id === state.heroId);
}

function getClassInfo() {
  const hero = getHero();
  return hero ? DATA.classes[hero.class] : null;
}

function isSkillAllowed(skillName) {
  const cls = getClassInfo();
  if (!cls) return true;
  const sk = DATA.skills[skillName];
  if (!sk) return false;
  if (cls.type === "Might" && sk.magic === false) return false;
  if (cls.type === "Magic" && sk.might === false) return false;
  if (skillName === "Thaumaturgy" && cls.type === "Might") return false;
  if (skillName === "Recruitment" && cls.type === "Magic") return false;
  if (skillName === "Combat" && cls.type === "Magic") return false;
  return true;
}

function factionSkillName() {
  return DATA.factions[state.faction].skill;
}

function applyStaticI18n() {
  document.documentElement.lang = lang;
  document.title = t("title");
  document.getElementById("hdrTitle").textContent = t("title");
  document.getElementById("hdrSubtitle").textContent = t("subtitle");
  document.getElementById("lblHero").textContent = t("hero");
  document.getElementById("lblFaction").textContent = t("faction");
  document.getElementById("lblClass").textContent = t("class");
  document.getElementById("lblHeroSelect").textContent = t("heroSelect");
  document.getElementById("lblWheel").textContent = t("skillWheel");
  document.getElementById("legMight").textContent = t("might");
  document.getElementById("legMagic").textContent = t("magic");
  document.getElementById("legGeneral").textContent = t("general");
  document.getElementById("legFaction").textContent = t("factionSkill");
  document.getElementById("lblSubclass").textContent = t("subclass");
  document.getElementById("lblSynergies").textContent = t("synergies");
  document.getElementById("lblLevelPlan").textContent = t("levelPlan");
  document.getElementById("levelPlanHint").textContent = t("levelPlanHint");
  document.getElementById("lblTargetLevel").textContent = t("targetLevel");
  document.getElementById("btnReset").textContent = t("reset");
  document.getElementById("btnExport").textContent = t("exportJson");
  document.getElementById("btnImport").textContent = t("importJson");
  document.getElementById("btnRemoveSkill").textContent = t("remove");
  document.getElementById("lblTier").textContent = t("tierBasic").replace("Basic", lang === "ru" ? "Уровень" : "Tier");
  document.getElementById("btnGenOffers").textContent = lang === "ru" ? "Случайные 3" : "Random ×3";
  document.getElementById("btnApplyPlan").textContent = lang === "ru" ? "Применить" : "Apply plan";
  document.getElementById("btnClearPlan").textContent = t("clearPlan");
  document.getElementById("footerText").innerHTML =
    t("footerData") + ' <a href="https://wiki.hoodedhorse.com/Heroes_of_Might_and_Magic_Olden_Era/Skills" target="_blank">' + t("footerWiki") + "</a> · " +
    '<a href="HoMM_Olden_Era_Skills.md">' + t("footerGuide") + "</a>";
  document.getElementById("selLang").value = lang;
}

function initHeroFromSelection() {
  const hero = getHero();
  if (!hero) return;
  state.faction = hero.faction;
  state.slots = Array(SLOT_COUNT).fill(null);
  const fSkill = factionSkillName();
  state.slots[0] = {
    skill: fSkill,
    tier: hero.start?.some(s => s.skill === fSkill && s.tier === "Advanced") ? 2 : 1,
    advSub: null,
    expSub: null,
    locked: true
  };
  let idx = 1;
  (hero.start || []).forEach(s => {
    const skill = normSkill(s.skill);
    if (skill === fSkill) {
      if (s.tier === "Advanced") state.slots[0].tier = 2;
      return;
    }
    if (idx < SLOT_COUNT) {
      state.slots[idx++] = {
        skill,
        tier: s.tier === "Advanced" ? 2 : 1,
        advSub: null,
        expSub: null,
        locked: true
      };
    }
  });
  if (hero.subclassHint) {
    const subs = DATA.classes[hero.class]?.subclasses || {};
    if (subs[hero.subclassHint]) state.targetSubclass = hero.subclassHint;
  }
  state.selectedSlot = null;
  levelPlan = {};
  levelOffers = {};
  renderAll();
}

function populateSelects() {
  const selF = document.getElementById("selFaction");
  selF.innerHTML = Object.keys(DATA.factions).map(f =>
    `<option value="${f}">${factionLabel(f)}</option>`).join("");
  selF.value = state.faction;
  selF.onchange = () => {
    state.faction = selF.value;
    updateClassHeroSelects();
    const first = DATA.heroes.find(h => h.faction === state.faction);
    if (first) { state.heroId = first.id; initHeroFromSelection(); }
  };
  updateClassHeroSelects();
}

function updateClassHeroSelects() {
  const heroes = DATA.heroes.filter(h => h.faction === state.faction);
  const classes = [...new Set(heroes.map(h => h.class))];
  const selC = document.getElementById("selClass");
  selC.innerHTML = classes.map(c => `<option value="${c}">${c}</option>`).join("");
  selC.onchange = updateHeroSelect;
  updateHeroSelect();
}

function updateHeroSelect() {
  const cls = document.getElementById("selClass").value;
  const heroes = DATA.heroes.filter(h => h.faction === state.faction && h.class === cls);
  const selH = document.getElementById("selHero");
  selH.innerHTML = heroes.map(h => `<option value="${h.id}">${h.name}</option>`).join("");
  if (!heroes.find(h => h.id === state.heroId)) state.heroId = heroes[0]?.id;
  selH.value = state.heroId;
  selH.onchange = () => { state.heroId = selH.value; initHeroFromSelection(); };
  initHeroFromSelection();
}

function renderHeroCard() {
  const hero = getHero();
  const card = document.getElementById("heroCard");
  const stats = document.getElementById("heroStats");
  if (!hero) { card.innerHTML = ""; stats.innerHTML = ""; return; }
  const cls = DATA.classes[hero.class];
  card.innerHTML = `
    <div class="spec-title">${hero.specialty}</div>
    <div class="spec-desc">${heroDesc(hero)}</div>
    <div class="tags">
      <span class="tag ${cls?.type === "Might" ? "might" : "magic"}">${cls?.type || ""}</span>
      <span class="tag">${hero.class}</span>
      ${hero.universal ? `<span class="tag">${t("universal")}</span>` : ""}
      ${hero.subclassHint ? `<span class="tag">→ ${hero.subclassHint}</span>` : ""}
    </div>
  `;
  const startTxt = (hero.start || []).map(s => `${s.tier} ${normSkill(s.skill)}`).join(", ") || "—";
  stats.innerHTML = `
    <div><b>${t("faction")}:</b> ${factionLabel(hero.faction)}</div>
    <div><b>${t("startingSkills")}:</b> ${startTxt}</div>
    <div><b>${t("spell")}:</b> ${hero.spell || "—"}</div>
    <div><b>${t("slotsUsed")}:</b> ${usedSlots()}/8</div>
  `;
}

function usedSlots() {
  return state.slots.filter(Boolean).length;
}

function renderWheel() {
  const wheel = document.getElementById("wheel");
  wheel.innerHTML = "";
  const reqSkills = getRequiredSkills();
  const W = wheel.offsetWidth || 520;
  const R = W * 0.36;
  const cx = W / 2, cy = W / 2;

  const center = document.createElement("div");
  center.className = "wheel-center";
  center.innerHTML = `
    <div class="label">${t("factionCenter")}</div>
    <div class="name">${factionSkillName()}</div>
    <div class="tier">${state.slots[0] ? tierLabel(state.slots[0].tier) : t("tierBasic")}</div>
  `;
  wheel.appendChild(center);

  for (let i = 0; i < SLOT_COUNT; i++) {
    const angle = (-90 + i * (360 / SLOT_COUNT)) * Math.PI / 180;
    const x = cx + R * Math.cos(angle) - 59;
    const y = cy + R * Math.sin(angle) - 46;
    const slot = state.slots[i];
    const el = document.createElement("div");
    el.className = "slot";
    el.style.left = x + "px";
    el.style.top = y + "px";
    if (!slot) {
      el.classList.add("empty");
      el.innerHTML = `<div class="skill-name">${t("slot")} ${i + 1}</div><div class="tier">${t("addSkillSlot")}</div>`;
    } else {
      const sk = DATA.skills[slot.skill];
      el.classList.add("cat-" + (sk?.cat || "general"));
      if (reqSkills.includes(slot.skill)) el.classList.add("required");
      const subs = [];
      if (slot.tier >= 2 && slot.advSub) subs.push("A: " + slot.advSub);
      if (slot.tier >= 3 && slot.expSub) subs.push("E: " + slot.expSub);
      el.innerHTML = `
        <div class="skill-name">${slot.skill}</div>
        <div class="tier">${tierLabel(slot.tier)}</div>
        <div class="subs">${subs.join("<br>") || (slot.tier >= 2 ? t("chooseSub") : "")}</div>
      `;
    }
    if (state.selectedSlot === i) el.classList.add("active");
    el.onclick = () => selectSlot(i);
    wheel.appendChild(el);
  }
}

function selectSlot(i) {
  state.selectedSlot = i;
  renderWheel();
  renderEditor();
}

function renderEditor() {
  const ed = document.getElementById("skillEditor");
  const i = state.selectedSlot;
  if (i === null) { ed.hidden = true; return; }
  ed.hidden = false;
  const slot = state.slots[i];
  document.getElementById("editorTitle").textContent = slot ? slot.skill : `${t("slot")} ${i + 1}`;

  const selTier = document.getElementById("selTier");
  if (!slot) {
    selTier.innerHTML = `<option value="0">${t("choose")}</option>`;
    selTier.disabled = true;
    renderSkillPicker(i);
    document.getElementById("btnRemoveSkill").onclick = null;
    return;
  }
  selTier.disabled = slot.locked;
  selTier.innerHTML = [1, 2, 3].map(tier =>
    `<option value="${tier}" ${slot.tier === tier ? "selected" : ""}>${tierLabel(tier)}</option>`).join("");
  selTier.onchange = () => {
    slot.tier = +selTier.value;
    if (slot.tier < 2) slot.advSub = null;
    if (slot.tier < 3) slot.expSub = null;
    renderAll();
  };
  document.getElementById("btnRemoveSkill").onclick = () => {
    if (slot.locked) return;
    state.slots[i] = null;
    state.selectedSlot = i;
    renderAll();
  };
  renderSubPicks(slot);
}

function renderSkillPicker(slotIndex) {
  const subPicks = document.getElementById("subPicks");
  const used = new Set(state.slots.filter(Boolean).map(s => s.skill));
  const options = Object.keys(DATA.skills)
    .filter(name => !DATA.skills[name].faction)
    .filter(name => isSkillAllowed(name))
    .filter(name => !used.has(name))
    .sort();
  subPicks.innerHTML = `
    <label>${t("addSkill")} ${slotIndex + 1}</label>
    <select id="pickSkill">
      <option value="">${t("choose")}</option>
      ${options.map(o => `<option value="${o}">${o}</option>`).join("")}
    </select>
  `;
  document.getElementById("pickSkill").onchange = (e) => {
    const skill = e.target.value;
    if (!skill) return;
    state.slots[slotIndex] = { skill, tier: 1, advSub: null, expSub: null, locked: false };
    renderAll();
    selectSlot(slotIndex);
  };
}

function renderSubPicks(slot) {
  const subPicks = document.getElementById("subPicks");
  const sk = DATA.skills[slot.skill];
  if (!sk) { subPicks.innerHTML = ""; return; }
  let html = "";
  if (slot.tier >= 2 && sk.adv?.length) {
    html += `<label>${t("advSub")}</label>
      <select id="pickAdv">${sk.adv.map(s =>
        `<option value="${s}" ${slot.advSub === s ? "selected" : ""}>${s}</option>`).join("")}</select>`;
  }
  if (slot.tier >= 3 && sk.exp?.length) {
    html += `<label>${t("expSub")}</label>
      <select id="pickExp">${sk.exp.map(s =>
        `<option value="${s}" ${slot.expSub === s ? "selected" : ""}>${s}</option>`).join("")}</select>`;
  }
  subPicks.innerHTML = html;
  const pa = document.getElementById("pickAdv");
  if (pa) pa.onchange = () => { slot.advSub = pa.value; renderAll(); };
  const pe = document.getElementById("pickExp");
  if (pe) pe.onchange = () => { slot.expSub = pe.value; renderAll(); };
}

function getRequiredSkills() {
  if (!state.targetSubclass) return [];
  const hero = getHero();
  if (!hero) return [];
  const subs = DATA.classes[hero.class]?.subclasses?.[state.targetSubclass];
  return subs ? subs.skills.map(normSkill) : [];
}

function renderSubclasses() {
  const hero = getHero();
  const list = document.getElementById("subclassList");
  if (!hero) { list.innerHTML = ""; return; }
  const subs = DATA.classes[hero.class]?.subclasses || {};
  list.innerHTML = Object.entries(subs).map(([name, data]) => `
    <div class="subclass-item ${state.targetSubclass === name ? "selected" : ""}" data-sub="${name}">
      <div class="title">${name}</div>
      <div class="bonus">${subclassBonus(data)}</div>
    </div>
  `).join("");
  list.querySelectorAll(".subclass-item").forEach(el => {
    el.onclick = () => {
      state.targetSubclass = el.dataset.sub;
      renderAll();
    };
  });
}

function skillLevel(skillName) {
  const s = state.slots.find(sl => sl && sl.skill === skillName);
  return s ? s.tier : 0;
}

function renderRequirements() {
  const reqList = document.getElementById("reqList");
  const bar = document.getElementById("subProgressBar");
  const txt = document.getElementById("subProgressText");
  const alerts = document.getElementById("buildAlerts");
  const req = getRequiredSkills();
  if (!req.length) {
    reqList.innerHTML = "";
    bar.style.width = "0%";
    txt.textContent = t("selectSubclass");
    alerts.innerHTML = "";
    return;
  }
  let done = 0;
  reqList.innerHTML = req.map(skill => {
    const tier = skillLevel(skill);
    const cls = tier >= 3 ? "done" : tier > 0 ? "pending" : "missing";
    if (tier >= 3) done++;
    const chance = getClassInfo()?.skillChances?.[skill];
    const ch = chance !== undefined ? ` · ${chance}%${t("roll")}` : "";
    return `<div class="req ${cls}"><span>${skill}</span><span>${tier >= 3 ? t("expertDone") : tier > 0 ? tierLabel(tier) : t("none")}${ch}</span></div>`;
  }).join("");
  bar.style.width = (done / req.length * 100) + "%";
  txt.textContent = t("subclassProgress", { done, total: req.length });

  const used = usedSlots();
  const extra = state.slots.filter(Boolean).filter(s => !req.includes(s.skill) && !DATA.skills[s.skill]?.faction);
  let alertHtml = "";
  if (done === req.length) alertHtml += `<div class="alert ok">${t("subclassUnlocked")}</div>`;
  else if (used >= 8 && done < req.length) alertHtml += `<div class="alert">${t("slotsFullNoSubclass")}</div>`;
  else if (extra.length > 2) alertHtml += `<div class="alert warn">${t("extraSkillsWarn", { n: extra.length })}</div>`;
  if (used < 8) alertHtml += `<div class="alert ok">${t("freeSlots", { n: 8 - used })}</div>`;
  alerts.innerHTML = alertHtml;
}

function hasSubskill(slot, subName) {
  if (!slot || !subName) return true;
  const sk = DATA.skills[slot.skill];
  if (!sk) return false;
  if (slot.advSub === subName || slot.expSub === subName) return true;
  if (slot.tier >= 2 && sk.adv?.includes(subName)) return true;
  if (slot.tier >= 3 && sk.exp?.includes(subName)) return true;
  return false;
}

function renderSynergies() {
  const list = document.getElementById("synergyList");
  const skillMap = new Map();
  state.slots.filter(Boolean).forEach(s => skillMap.set(s.skill, s));

  const items = SYN.map(syn => {
    const need = normSkill(syn.needs);
    const slotA = skillMap.get(normSkill(syn.skill));
    const slotB = skillMap.get(need);
    const hasA = !!slotA;
    const hasB = !!slotB;
    const subOk = !syn.sub || hasSubskill(slotA, syn.sub);
    const active = hasA && hasB && subOk;
    const potential = hasA && !hasB;
    const desc = lang === "ru" ? syn.descRu : syn.descEn;
    return { ...syn, active, potential, desc, need };
  }).filter(x => x.active || x.potential);

  if (!items.length) {
    list.innerHTML = `<div class="hint">${t("noSynergies")}</div>`;
    return;
  }
  list.innerHTML = items.map(item => {
    const cls = item.active ? "active" : "potential";
    const extra = item.active ? "" : " · " + t("synergyNeeds", { skill: item.need, tier: "Basic" });
    const sub = item.sub ? ` [${item.sub}]` : "";
    return `<div class="synergy-item ${cls}"><b>${item.skill}${sub}</b> + ${item.need}: ${item.desc}${extra}</div>`;
  }).join("");
}

function allowedSkillsForLevel() {
  return Object.keys(DATA.skills)
    .filter(n => !DATA.skills[n].faction)
    .filter(n => isSkillAllowed(n))
    .sort();
}

function weightedPick(count, exclude) {
  const chances = getClassInfo()?.skillChances || {};
  const pool = allowedSkillsForLevel().filter(s => !exclude.has(s));
  if (!pool.length) return [];
  const weights = pool.map(s => ({ s, w: chances[s] || 1 }));
  const picks = [];
  for (let i = 0; i < count && weights.length; i++) {
    const total = weights.reduce((a, b) => a + b.w, 0);
    let r = Math.random() * total;
    let idx = 0;
    for (let j = 0; j < weights.length; j++) {
      r -= weights[j].w;
      if (r <= 0) { idx = j; break; }
    }
    picks.push(weights[idx].s);
    weights.splice(idx, 1);
  }
  return picks;
}

function simulatePlanSlots() {
  const hero = getHero();
  if (!hero) return { ok: false, count: 0, skills: {} };
  const fSkill = factionSkillName();
  const skillTiers = {};
  skillTiers[fSkill] = hero.start?.some(s => normSkill(s.skill) === fSkill && s.tier === "Advanced") ? 2 : 1;
  (hero.start || []).forEach(s => {
    const sk = normSkill(s.skill);
    if (sk === fSkill) return;
    skillTiers[sk] = s.tier === "Advanced" ? 2 : 1;
  });
  const target = +document.getElementById("selTargetLevel").value || 25;
  for (let lv = 2; lv <= target; lv++) {
    const pick = levelPlan[lv];
    if (!pick) continue;
    const sk = normSkill(pick);
    if (!skillTiers[sk]) skillTiers[sk] = 1;
    else if (skillTiers[sk] < 3) skillTiers[sk]++;
  }
  return { ok: Object.keys(skillTiers).length <= 8, count: Object.keys(skillTiers).length, skills: skillTiers };
}

function renderLevelPlan() {
  const rows = document.getElementById("levelRows");
  const status = document.getElementById("levelPlanStatus");
  const selTarget = document.getElementById("selTargetLevel");
  if (!selTarget.options.length) {
    selTarget.innerHTML = Array.from({ length: 24 }, (_, i) => {
      const lv = i + 2;
      return `<option value="${lv}" ${lv === 25 ? "selected" : ""}>${lv}</option>`;
    }).join("");
  }
  const target = +selTarget.value || 25;
  const allowed = allowedSkillsForLevel();
  let html = "";
  for (let lv = 2; lv <= target; lv++) {
    const offers = levelOffers[lv] || ["", "", ""];
    const pick = levelPlan[lv] || "";
    html += `<div class="level-row" data-lv="${lv}">
      <span class="lvl">${lv}</span>
      ${[0, 1, 2].map(i => `<select class="offer" data-lv="${lv}" data-i="${i}">
        <option value="">${t("choose")}</option>
        ${allowed.map(s => `<option value="${s}" ${offers[i] === s ? "selected" : ""}>${s}</option>`).join("")}
      </select>`).join("")}
    </div>`;
    html += `<div class="level-row" style="margin-bottom:6px">
      <span></span>
      <select class="pick" data-lv="${lv}" style="grid-column: span 3">
        <option value="">${t("pickSkill")}</option>
        ${allowed.map(s => `<option value="${s}" ${pick === s ? "selected" : ""}>${pick === s ? "→ " : ""}${s}</option>`).join("")}
      </select>
    </div>`;
  }
  rows.innerHTML = html;

  rows.querySelectorAll(".offer").forEach(el => {
    el.onchange = () => {
      const lv = +el.dataset.lv;
      if (!levelOffers[lv]) levelOffers[lv] = ["", "", ""];
      levelOffers[lv][+el.dataset.i] = el.value;
    };
  });
  rows.querySelectorAll(".pick").forEach(el => {
    el.onchange = () => {
      const lv = +el.dataset.lv;
      if (el.value) levelPlan[lv] = el.value;
      else delete levelPlan[lv];
      renderLevelPlanStatus();
    };
  });

  renderLevelPlanStatus();
}

function renderLevelPlanStatus() {
  const status = document.getElementById("levelPlanStatus");
  const sim = simulatePlanSlots();
  if (sim.ok) {
    status.innerHTML = `<div class="alert ok">${t("planOk", { n: sim.count })}</div>`;
  } else {
    status.innerHTML = `<div class="alert">${t("planConflict")} (${sim.count}/8)</div>`;
  }
}

function generateOffers() {
  levelOffers = {};
  const target = +document.getElementById("selTargetLevel").value || 25;
  const taken = new Set();
  const hero = getHero();
  if (hero) {
    taken.add(factionSkillName());
    (hero.start || []).forEach(s => taken.add(normSkill(s.skill)));
  }
  for (let lv = 2; lv <= target; lv++) {
    levelOffers[lv] = weightedPick(3, taken);
    if (levelPlan[lv]) taken.add(normSkill(levelPlan[lv]));
  }
  renderLevelPlan();
}

function rebuildSlotsFromPlan() {
  const hero = getHero();
  if (!hero) return;
  state.faction = hero.faction;
  state.slots = Array(SLOT_COUNT).fill(null);
  const fSkill = factionSkillName();
  state.slots[0] = {
    skill: fSkill,
    tier: hero.start?.some(s => normSkill(s.skill) === fSkill && s.tier === "Advanced") ? 2 : 1,
    advSub: null, expSub: null, locked: true
  };
  let idx = 1;
  (hero.start || []).forEach(s => {
    const skill = normSkill(s.skill);
    if (skill === fSkill) {
      if (s.tier === "Advanced") state.slots[0].tier = 2;
      return;
    }
    if (idx < SLOT_COUNT) {
      state.slots[idx++] = { skill, tier: s.tier === "Advanced" ? 2 : 1, advSub: null, expSub: null, locked: true };
    }
  });
  const sim = simulatePlanSlots();
  Object.entries(sim.skills).forEach(([skill, tier]) => {
    const existing = state.slots.find(s => s && s.skill === skill);
    if (existing) { existing.tier = Math.max(existing.tier, tier); return; }
    let slotIdx = state.slots.findIndex(s => !s);
    if (slotIdx < 0) return;
    state.slots[slotIdx] = { skill, tier, advSub: null, expSub: null, locked: false };
  });
}

function applyLevelPlan() {
  const sim = simulatePlanSlots();
  if (!sim.ok) { alert(t("planConflict")); return; }
  rebuildSlotsFromPlan();
  renderAll();
}

function clearLevelPlan() {
  levelPlan = {};
  levelOffers = {};
  renderLevelPlan();
}

function renderAll() {
  renderHeroCard();
  renderWheel();
  renderEditor();
  renderSubclasses();
  renderRequirements();
  renderSynergies();
  renderLevelPlan();
}

document.getElementById("selLang").onchange = (e) => {
  lang = e.target.value;
  localStorage.setItem("hoe_builder_lang", lang);
  applyStaticI18n();
  populateSelects();
  renderAll();
};

document.getElementById("selTargetLevel").onchange = () => renderLevelPlan();
document.getElementById("btnGenOffers").onclick = generateOffers;
document.getElementById("btnApplyPlan").onclick = applyLevelPlan;
document.getElementById("btnClearPlan").onclick = clearLevelPlan;

document.getElementById("btnReset").onclick = () => initHeroFromSelection();

document.getElementById("btnExport").onclick = () => {
  const hero = getHero();
  const payload = {
    version: 2,
    lang,
    hero: hero?.name,
    heroId: state.heroId,
    faction: state.faction,
    targetSubclass: state.targetSubclass,
    slots: state.slots,
    levelPlan
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `homm-oe-build-${hero?.id || "custom"}.json`;
  a.click();
};

document.getElementById("btnImport").onclick = () => document.getElementById("fileImport").click();
document.getElementById("fileImport").onchange = (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const data = JSON.parse(reader.result);
      if (data.lang) { lang = data.lang; document.getElementById("selLang").value = lang; applyStaticI18n(); }
      if (data.heroId) state.heroId = data.heroId;
      if (data.faction) state.faction = data.faction;
      if (data.targetSubclass) state.targetSubclass = data.targetSubclass;
      if (data.slots) state.slots = data.slots;
      if (data.levelPlan) levelPlan = data.levelPlan;
      populateSelects();
      renderAll();
    } catch (err) { alert(t("importError") + err.message); }
  };
  reader.readAsText(file);
};

applyStaticI18n();
populateSelects();
if (DATA.heroes?.length) {
  state.heroId = DATA.heroes[0].id;
  initHeroFromSelection();
}
