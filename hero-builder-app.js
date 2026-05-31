const DATA = window.HOE_BUILDER_DATA;
const SYN = window.HOE_BUILDER_SYNERGIES || [];
const I18N = window.HOE_BUILDER_I18N;
const DISP = window.HOE_BUILDER_DISPLAY;
const CORE = window.HOE_BUILDER_CORE;
const SLOT_COUNT = CORE.SLOT_COUNT;
let lang = localStorage.getItem("hoe_builder_lang") || "ru";
let state = {
  faction: "Temple",
  classType: "Might",
  selectedSlot: null,
  targetSubclass: null,
  slots: CORE.buildConfiguratorSlots(DATA, "Temple")
};

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

function localizeGameText(text) {
  if (lang !== "ru" || !DISP || !text) return text;
  const pairs = [];
  Object.keys(DISP.skills.en || {}).forEach((k) => pairs.push([k, DISP.skill("ru", k)]));
  Object.keys(DISP.subskills.en || {}).forEach((k) => pairs.push([k, DISP.subskill("ru", k)]));
  Object.keys(DISP.subclasses.en || {}).forEach((k) => pairs.push([k, DISP.subclass("ru", k)]));
  pairs.sort((a, b) => b[0].length - a[0].length);
  let out = text;
  pairs.forEach(([en, ru]) => {
    if (en && ru && en !== ru) out = out.split(en).join(ru);
  });
  return out;
}

function subclassBonus(data) {
  return lang === "ru" ? (data.bonusRu || data.bonus || data.bonusEn) : (data.bonusEn || data.bonus || data.bonusRu);
}

function factionLabel(f) {
  return (I18N[lang].factions && I18N[lang].factions[f]) || f;
}

function skillLabel(skillName) {
  if (!skillName) return "";
  const key = normSkill(skillName);
  return DISP ? DISP.skill(lang, key) : key;
}

function subskillLabel(subName) {
  if (!subName) return "";
  return DISP ? DISP.subskill(lang, subName) : subName;
}

function subclassLabel(subName) {
  if (!subName) return "";
  return DISP ? DISP.subclass(lang, subName) : subName;
}

function classTypeLabel(type) {
  if (type === "Might") return t("classMight");
  if (type === "Magic") return t("classMagic");
  return type || "";
}

function normSkill(name) {
  return CORE.normSkill(DATA, name);
}

function getClassTemplate() {
  return CORE.findClassTemplate(DATA, state.faction, state.classType);
}

function isSkillAllowed(skillName) {
  return CORE.isSkillAllowed(DATA, getClassTemplate(), skillName);
}

function factionSkillName() {
  return CORE.factionSkillName(DATA, state.faction);
}

function availableClassTypes() {
  const types = new Set();
  Object.values(DATA.classes).forEach((c) => {
    if (c.faction === state.faction) types.add(c.type);
  });
  return [...types];
}

function resetBuild() {
  state.slots = CORE.buildConfiguratorSlots(DATA, state.faction);
  state.selectedSlot = null;
  state.targetSubclass = null;
}

function initFromConfig() {
  resetBuild();
  renderAll();
  syncUrl();
}

function applyStaticI18n() {
  document.documentElement.lang = lang;
  document.title = t("title");
  document.getElementById("hdrTitle").textContent = t("title");
  document.getElementById("hdrSubtitle").textContent = t("subtitle");
  document.getElementById("lblConfig").textContent = t("config");
  document.getElementById("lblFaction").textContent = t("faction");
  document.getElementById("lblClassType").textContent = t("classType");
  document.getElementById("lblWheel").textContent = t("skillWheel");
  document.getElementById("legMight").textContent = t("might");
  document.getElementById("legMagic").textContent = t("magic");
  document.getElementById("legGeneral").textContent = t("general");
  document.getElementById("legFaction").textContent = t("factionSkill");
  document.getElementById("lblSubclass").textContent = t("subclass");
  document.getElementById("lblSynergies").textContent = t("synergies");
  document.getElementById("lblLevelCalc").textContent = t("levelCalc");
  document.getElementById("levelCalcHint").textContent = t("levelCalcHint");
  document.getElementById("lblLevelBreakdown").textContent = t("levelBreakdown");
  document.getElementById("btnReset").textContent = t("reset");
  document.getElementById("btnExport").textContent = t("exportJson");
  document.getElementById("btnImport").textContent = t("importJson");
  document.getElementById("btnShare").textContent = t("shareLink");
  document.getElementById("btnRemoveSkill").textContent = t("remove");
  document.getElementById("lblTier").textContent = t("tierHdr");
  document.getElementById("footerText").innerHTML =
    t("footerData") + ' <a href="https://wiki.hoodedhorse.com/Heroes_of_Might_and_Magic_Olden_Era/Skills" target="_blank">' + t("footerWiki") + "</a> · " +
    '<a href="HoMM_Olden_Era_Skills.md">' + t("footerGuide") + "</a>";
  document.getElementById("selLang").value = lang;
}

function populateSelects() {
  const selF = document.getElementById("selFaction");
  selF.innerHTML = Object.keys(DATA.factions).map(f =>
    `<option value="${f}">${factionLabel(f)}</option>`).join("");
  selF.value = state.faction;
  selF.onchange = () => {
    state.faction = selF.value;
    const types = availableClassTypes();
    if (!types.includes(state.classType)) state.classType = types[0] || "Might";
    populateClassTypeSelect();
    initFromConfig();
  };
  populateClassTypeSelect();
}

function populateClassTypeSelect() {
  const selT = document.getElementById("selClassType");
  const types = availableClassTypes();
  selT.innerHTML = types.map(tp =>
    `<option value="${tp}">${classTypeLabel(tp)}</option>`).join("");
  if (!types.includes(state.classType)) state.classType = types[0] || "Might";
  selT.value = state.classType;
  selT.onchange = () => {
    state.classType = selT.value;
    state.targetSubclass = null;
    initFromConfig();
  };
}

function renderConfigPanel() {
  const card = document.getElementById("configCard");
  const stats = document.getElementById("heroStats");
  const fSkill = factionSkillName();
  card.innerHTML = `
    <div class="spec-title">${t("abstractHero")}</div>
    <div class="spec-desc">${t("abstractHeroDesc")}</div>
    <div class="tags">
      <span class="tag ${state.classType === "Might" ? "might" : "magic"}">${classTypeLabel(state.classType)}</span>
      <span class="tag">${factionLabel(state.faction)}</span>
      <span class="tag">${skillLabel(fSkill)}</span>
    </div>
  `;
  stats.innerHTML = `
    <div><b>${t("faction")}:</b> ${factionLabel(state.faction)}</div>
    <div><b>${t("classType")}:</b> ${classTypeLabel(state.classType)}</div>
    <div><b>${t("factionSkill")}:</b> ${skillLabel(fSkill)} (${t("tierBasic")})</div>
    <div><b>${t("slotsUsed")}:</b> ${usedSlots()}/8</div>
  `;
}

function usedSlots() {
  return CORE.usedSlotCount(state.slots);
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
  center.style.borderColor = DATA.factions[state.faction]?.color || undefined;
  center.innerHTML = `
    <div class="label">${t("factionCenter")}</div>
    <div class="name">${skillLabel(factionSkillName())}</div>
    <div class="tier">${state.slots[0] ? tierLabel(state.slots[0].tier) : t("tierBasic")}</div>
  `;
  center.onclick = () => selectSlot(0);
  if (state.selectedSlot === 0) center.classList.add("active");
  wheel.appendChild(center);

  for (let i = 1; i < SLOT_COUNT; i++) {
    const angle = (-90 + (i - 1) * (360 / (SLOT_COUNT - 1))) * Math.PI / 180;
    const x = cx + R * Math.cos(angle) - 59;
    const y = cy + R * Math.sin(angle) - 46;
    const slot = state.slots[i];
    const el = document.createElement("div");
    el.className = "slot";
    el.style.left = x + "px";
    el.style.top = y + "px";
    if (!slot) {
      el.classList.add("empty");
      el.innerHTML = `<div class="skill-name">${t("slot")} ${i}</div><div class="tier">${t("addSkillSlot")}</div>`;
    } else {
      const sk = DATA.skills[slot.skill];
      el.classList.add("cat-" + (sk?.cat || "general"));
      if (reqSkills.includes(slot.skill)) el.classList.add("required");
      const subs = [];
      if (slot.tier >= 2 && slot.advSub) subs.push("A: " + subskillLabel(slot.advSub));
      if (slot.tier >= 3 && slot.expSub) subs.push("E: " + subskillLabel(slot.expSub));
      el.innerHTML = `
        <div class="skill-name">${skillLabel(slot.skill)}</div>
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
  document.getElementById("editorTitle").textContent = slot ? skillLabel(slot.skill) : `${t("slot")} ${i}`;

  const selTier = document.getElementById("selTier");
  if (!slot) {
    selTier.innerHTML = `<option value="0">${t("choose")}</option>`;
    selTier.disabled = true;
    renderSkillPicker(i);
    document.getElementById("btnRemoveSkill").onclick = null;
    return;
  }
  selTier.disabled = false;
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
    .sort((a, b) => skillLabel(a).localeCompare(skillLabel(b), lang));
  subPicks.innerHTML = `
    <label>${t("addSkill")} ${slotIndex}</label>
    <select id="pickSkill">
      <option value="">${t("choose")}</option>
      ${options.map(o => `<option value="${o}">${skillLabel(o)}</option>`).join("")}
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
        `<option value="${s}" ${slot.advSub === s ? "selected" : ""}>${subskillLabel(s)}</option>`).join("")}</select>`;
  }
  if (slot.tier >= 3 && sk.exp?.length) {
    html += `<label>${t("expSub")}</label>
      <select id="pickExp">${sk.exp.map(s =>
        `<option value="${s}" ${slot.expSub === s ? "selected" : ""}>${subskillLabel(s)}</option>`).join("")}</select>`;
  }
  subPicks.innerHTML = html;
  const pa = document.getElementById("pickAdv");
  if (pa) pa.onchange = () => { slot.advSub = pa.value; renderAll(); };
  const pe = document.getElementById("pickExp");
  if (pe) pe.onchange = () => { slot.expSub = pe.value; renderAll(); };
}

function getRequiredSkills() {
  return CORE.getRequiredSkills(DATA, getClassTemplate(), state.targetSubclass);
}

function renderSubclasses() {
  const list = document.getElementById("subclassList");
  const classInfo = getClassTemplate();
  const subs = classInfo?.subclasses || {};
  list.innerHTML = Object.entries(subs).map(([name, data]) => `
    <div class="subclass-item ${state.targetSubclass === name ? "selected" : ""}" data-sub="${name}">
      <div class="title">${subclassLabel(name)}</div>
      <div class="bonus">${subclassBonus(data)}</div>
    </div>
  `).join("");
  list.querySelectorAll(".subclass-item").forEach(el => {
    el.onclick = () => {
      state.targetSubclass = state.targetSubclass === el.dataset.sub ? null : el.dataset.sub;
      renderAll();
    };
  });
}

function skillLevel(skillName) {
  return CORE.skillLevel(state.slots, skillName);
}

function renderRequirements() {
  const reqList = document.getElementById("reqList");
  const bar = document.getElementById("subProgressBar");
  const txt = document.getElementById("subProgressText");
  const alerts = document.getElementById("buildAlerts");
  const req = getRequiredSkills();
  if (!req.length) {
    reqList.innerHTML = `<div class="hint">${t("selectSubclass")}</div>`;
    bar.style.width = "0%";
    txt.textContent = "";
    alerts.innerHTML = "";
    return;
  }
  let done = 0;
  reqList.innerHTML = req.map(skill => {
    const tier = skillLevel(skill);
    const cls = tier >= 3 ? "done" : tier > 0 ? "pending" : "missing";
    if (tier >= 3) done++;
    const chance = getClassTemplate()?.skillChances?.[skill];
    const ch = chance !== undefined ? ` · ${chance}%${t("roll")}` : "";
    return `<div class="req ${cls}"><span>${skillLabel(skill)}</span><span>${tier >= 3 ? t("expertDone") : tier > 0 ? tierLabel(tier) : t("none")}${ch}</span></div>`;
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

function synergyStatus(syn, skillMap) {
  return CORE.synergyStatus(DATA, syn, skillMap);
}

function synergyStatusNote(syn, status, skillMap) {
  const need = normSkill(syn.needs);
  const slotA = skillMap.get(normSkill(syn.skill));
  if (status === "active") return "";
  if (status === "partial") return t("synergyNeedsSub", { sub: subskillLabel(syn.sub), skill: skillLabel(syn.skill) });
  if (status === "potential") return t("synergyNeedsSkill", { skill: skillLabel(need) });
  if (!slotA) return t("synergyNeedsSkill", { skill: skillLabel(syn.skill) });
  return "";
}

function renderSynergyItem(item) {
  const sub = item.sub ? ` [${subskillLabel(item.sub)}]` : "";
  const note = item.statusNote ? `<div class="syn-status">${item.statusNote}</div>` : "";
  return `<div class="synergy-item ${item.status}"><b>${skillLabel(item.skill)}${sub}</b> + ${skillLabel(item.need)}: ${item.desc}${note}</div>`;
}

function renderSynergies() {
  const list = document.getElementById("synergyList");
  const skillMap = new Map();
  state.slots.filter(Boolean).forEach(s => skillMap.set(s.skill, s));

  if (!SYN.length) {
    list.innerHTML = `<div class="hint">${t("noSynergies")}</div>`;
    return;
  }

  const items = SYN.map(syn => {
    const need = normSkill(syn.needs);
    const status = synergyStatus(syn, skillMap);
    const desc = lang === "ru" ? syn.descRu : syn.descEn;
    return {
      ...syn,
      need,
      status,
      statusNote: synergyStatusNote(syn, status, skillMap),
      desc
    };
  });

  const active = items.filter(x => x.status === "active");
  const partial = items.filter(x => x.status === "partial");
  const potential = items.filter(x => x.status === "potential");
  const inactive = items.filter(x => x.status === "inactive");

  let html = `<div class="synergy-head">${t("synergyCount", { active: active.length, total: items.length })}</div>`;

  const sections = [
    ["synergySectionActive", active],
    ["synergySectionPartial", partial],
    ["synergySectionPotential", potential],
    ["synergySectionInactive", inactive]
  ];

  sections.forEach(([titleKey, group]) => {
    if (!group.length) return;
    html += `<div class="synergy-group-title">${t(titleKey)} (${group.length})</div>`;
    html += group.map(renderSynergyItem).join("");
  });

  list.innerHTML = html;
}

function computeBuildLevelCost() {
  const start = CORE.getConfiguratorStartingTiers(DATA, state.faction);
  const current = CORE.getCurrentSkillTiers(state.slots);
  return CORE.computeBuildLevelCost(start, current);
}

function renderLevelCalculator() {
  const summary = document.getElementById("levelCalcSummary");
  const status = document.getElementById("levelCalcStatus");
  const breakdownEl = document.getElementById("levelCalcBreakdown");
  const calc = computeBuildLevelCost();

  summary.innerHTML = `
    <div class="level-calc-stat"><span>${t("levelUpsNeeded")}</span><b>${calc.levelUps}</b></div>
    <div class="level-calc-stat"><span>${t("minHeroLevel")}</span><b>${calc.minHeroLevel}</b></div>
    <div class="level-calc-stat"><span>${t("newSkillsCount")}</span><b>${calc.newSkills}</b></div>
    <div class="level-calc-stat"><span>${t("tierUpgradesCount")}</span><b>${calc.tierUpgrades}</b></div>
  `;

  let alerts = "";
  if (!calc.slotsOk) alerts += `<div class="alert">${t("buildTooManySlots", { n: calc.skillCount })}</div>`;
  if (!calc.levelOk) alerts += `<div class="alert warn">${t("buildTooHighLevel", { n: calc.minHeroLevel })}</div>`;
  if (calc.feasible) alerts += `<div class="alert ok">${t("buildFeasible")}</div>`;
  status.innerHTML = alerts;

  if (!calc.breakdown.length) {
    breakdownEl.innerHTML = `<div class="hint">${t("none")}</div>`;
    return;
  }

  breakdownEl.innerHTML = calc.breakdown.map(step => {
    const cls = step.kind === "new" ? "new-skill" : "tier-up";
    const text = step.kind === "new"
      ? t("levelUpNewSkill", { lv: step.heroLevel, skill: skillLabel(step.skill) })
      : t("levelUpTier", { lv: step.heroLevel, skill: skillLabel(step.skill), tier: tierLabel(step.tier) });
    return `<div class="level-calc-row ${cls}">${text}</div>`;
  }).join("");
}

function buildExportPayload() {
  return {
    version: 3,
    lang,
    faction: state.faction,
    classType: state.classType,
    targetSubclass: state.targetSubclass,
    slots: state.slots
  };
}

function applyImportPayload(data) {
  if (data.lang) { lang = data.lang; document.getElementById("selLang").value = lang; applyStaticI18n(); }
  if (data.faction) state.faction = data.faction;
  if (data.classType) state.classType = data.classType;
  state.targetSubclass = data.targetSubclass || null;
  if (data.slots) state.slots = data.slots;
  else resetBuild();
  populateSelects();
  renderAll();
  syncUrl();
}

function encodeBuildToHash() {
  try {
    const raw = JSON.stringify(buildExportPayload());
    return "#" + btoa(unescape(encodeURIComponent(raw)));
  } catch (_) {
    return "";
  }
}

function decodeBuildFromHash(hash) {
  if (!hash || hash.length < 2) return null;
  try {
    const raw = hash.startsWith("#") ? hash.slice(1) : hash;
    return JSON.parse(decodeURIComponent(escape(atob(raw))));
  } catch (_) {
    return null;
  }
}

function syncUrl() {
  const hash = encodeBuildToHash();
  if (hash && location.hash !== hash) {
    history.replaceState(null, "", hash);
  }
}

function loadFromUrl() {
  const data = decodeBuildFromHash(location.hash);
  if (data) applyImportPayload(data);
}

function renderAll() {
  renderConfigPanel();
  renderWheel();
  renderEditor();
  renderSubclasses();
  renderRequirements();
  renderSynergies();
  renderLevelCalculator();
  syncUrl();
}

document.getElementById("selLang").onchange = (e) => {
  lang = e.target.value;
  localStorage.setItem("hoe_builder_lang", lang);
  applyStaticI18n();
  populateSelects();
  renderAll();
};

document.getElementById("btnReset").onclick = () => initFromConfig();

document.getElementById("btnExport").onclick = () => {
  const payload = buildExportPayload();
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `homm-oe-build-${state.faction}-${state.classType}.json`;
  a.click();
};

document.getElementById("btnShare").onclick = async () => {
  syncUrl();
  const url = location.href.split("#")[0] + encodeBuildToHash();
  try {
    await navigator.clipboard.writeText(url);
    alert(t("shareCopied"));
  } catch (_) {
    prompt(t("sharePrompt"), url);
  }
};

document.getElementById("btnImport").onclick = () => document.getElementById("fileImport").click();
document.getElementById("fileImport").onchange = (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      applyImportPayload(JSON.parse(reader.result));
    } catch (err) { alert(t("importError") + err.message); }
  };
  reader.readAsText(file);
  e.target.value = "";
};

window.addEventListener("hashchange", () => {
  const data = decodeBuildFromHash(location.hash);
  if (data) applyImportPayload(data);
});

applyStaticI18n();
populateSelects();
loadFromUrl();
if (!location.hash) renderAll();
