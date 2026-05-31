/**
 * HoMM Olden Era Hero Builder — pure build logic (browser + Node).
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.HOE_BUILDER_CORE = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  const SLOT_COUNT = 8;
  const MAX_PRACTICAL_LEVEL = 25;

  function normSkill(data, name) {
    return data.skillAliases[name] || name;
  }

  function factionSkillName(data, faction) {
    return data.factions[faction].skill;
  }

  function findClassTemplate(data, faction, classType) {
    if (!faction || !classType) return null;
    return Object.values(data.classes).find(
      c => c.faction === faction && c.type === classType
    ) || null;
  }

  function buildConfiguratorSlots(data, faction) {
    const slots = Array(SLOT_COUNT).fill(null);
    const fSkill = factionSkillName(data, faction);
    slots[0] = {
      skill: fSkill,
      tier: 1,
      advSub: null,
      expSub: null,
      locked: true
    };
    return slots;
  }

  function getConfiguratorStartingTiers(data, faction) {
    const fSkill = factionSkillName(data, faction);
    return { [fSkill]: 1 };
  }

  function isSkillAllowed(data, classInfo, skillName) {
    if (!classInfo) return true;
    const sk = data.skills[skillName];
    if (!sk) return false;
    if (classInfo.type === "Might" && sk.might === false) return false;
    if (classInfo.type === "Magic" && sk.magic === false) return false;
    if (skillName === "Thaumaturgy" && classInfo.type === "Might") return false;
    if (skillName === "Recruitment" && classInfo.type === "Magic") return false;
    if (skillName === "Combat" && classInfo.type === "Magic") return false;
    return true;
  }

  function buildInitialSlots(data, hero) {
    const slots = Array(SLOT_COUNT).fill(null);
    if (!hero) return slots;

    const fSkill = factionSkillName(data, hero.faction);
    slots[0] = {
      skill: fSkill,
      tier: hero.start?.some(s => normSkill(data, s.skill) === fSkill && s.tier === "Advanced") ? 2 : 1,
      advSub: null,
      expSub: null,
      locked: true
    };

    let idx = 1;
    (hero.start || []).forEach(s => {
      const skill = normSkill(data, s.skill);
      if (skill === fSkill) {
        if (s.tier === "Advanced") slots[0].tier = 2;
        return;
      }
      if (idx < SLOT_COUNT) {
        slots[idx++] = {
          skill,
          tier: s.tier === "Advanced" ? 2 : 1,
          advSub: null,
          expSub: null,
          locked: true
        };
      }
    });
    return slots;
  }

  function usedSlotCount(slots) {
    return slots.filter(Boolean).length;
  }

  function getRequiredSkills(data, classTemplate, targetSubclass) {
    if (!targetSubclass || !classTemplate) return [];
    const subs = classTemplate.subclasses?.[targetSubclass];
    return subs ? subs.skills.map(s => normSkill(data, s)) : [];
  }

  function skillLevel(slots, skillName) {
    const s = slots.find(sl => sl && sl.skill === skillName);
    return s ? s.tier : 0;
  }

  function subclassProgress(data, classTemplate, slots, targetSubclass) {
    const required = getRequiredSkills(data, classTemplate, targetSubclass);
    if (!required.length) {
      return { required, done: 0, total: 0, complete: false };
    }
    const done = required.filter(skill => skillLevel(slots, skill) >= 3).length;
    return {
      required,
      done,
      total: required.length,
      complete: done === required.length
    };
  }

  function hasSubskill(slot, subName) {
    if (!slot || !subName) return true;
    return slot.advSub === subName || slot.expSub === subName;
  }

  function synergyStatus(data, syn, skillMap) {
    const need = normSkill(data, syn.needs);
    const skillA = normSkill(data, syn.skill);
    const slotA = skillMap.get(skillA);
    const slotB = skillMap.get(need);
    const hasA = !!slotA;
    const hasB = !!slotB;
    const subOk = !syn.sub || hasSubskill(slotA, syn.sub);
    if (hasA && hasB && subOk) return "active";
    if (hasA && hasB && !subOk) return "partial";
    if (hasA && !hasB) return "potential";
    return "inactive";
  }

  function computeSynergies(data, synergies, slots) {
    const skillMap = new Map();
    slots.filter(Boolean).forEach(s => skillMap.set(s.skill, s));
    return synergies.map(syn => ({
      syn,
      need: normSkill(data, syn.needs),
      status: synergyStatus(data, syn, skillMap)
    }));
  }

  function getStartingSkillTiers(data, hero) {
    if (!hero) return {};
    const fSkill = factionSkillName(data, hero.faction);
    const tiers = {};
    tiers[fSkill] = hero.start?.some(s => normSkill(data, s.skill) === fSkill && s.tier === "Advanced") ? 2 : 1;
    (hero.start || []).forEach(s => {
      const sk = normSkill(data, s.skill);
      if (sk === fSkill) {
        if (s.tier === "Advanced") tiers[fSkill] = 2;
        return;
      }
      tiers[sk] = s.tier === "Advanced" ? 2 : 1;
    });
    return tiers;
  }

  function getCurrentSkillTiers(slots) {
    const tiers = {};
    slots.filter(Boolean).forEach(s => {
      tiers[s.skill] = Math.max(tiers[s.skill] || 0, s.tier);
    });
    return tiers;
  }

  function computeBuildLevelCost(startTiers, currentTiers, opts = {}) {
    const maxSlots = opts.slotCount ?? SLOT_COUNT;
    const maxLevel = opts.maxLevel ?? MAX_PRACTICAL_LEVEL;
    const steps = [];

    Object.entries(currentTiers).forEach(([skill, targetTier]) => {
      const startTier = startTiers[skill] || 0;
      for (let tier = startTier + 1; tier <= targetTier; tier++) {
        steps.push({
          skill,
          tier,
          kind: startTier === 0 && tier === 1 ? "new" : "tier"
        });
      }
    });

    steps.sort((a, b) => {
      if (a.kind !== b.kind) return a.kind === "new" ? -1 : 1;
      return a.skill.localeCompare(b.skill);
    });

    const breakdown = steps.map((step, i) => ({
      ...step,
      heroLevel: i + 2
    }));

    const levelUps = steps.length;
    const newSkills = steps.filter(s => s.kind === "new").length;
    const tierUpgrades = steps.filter(s => s.kind === "tier").length;
    const skillCount = Object.keys(currentTiers).length;
    const minHeroLevel = 1 + levelUps;
    const slotsOk = skillCount <= maxSlots;
    const levelOk = minHeroLevel <= maxLevel;

    return {
      levelUps,
      minHeroLevel,
      newSkills,
      tierUpgrades,
      skillCount,
      breakdown,
      feasible: slotsOk && levelOk,
      slotsOk,
      levelOk
    };
  }

  function validateBuild(ctx) {
    const { data, faction, classType, slots, targetSubclass } = ctx;
    const errors = [];
    const warnings = [];

    if (!faction || !classType) {
      errors.push("no_config");
      return { ok: false, errors, warnings };
    }

    const classInfo = findClassTemplate(data, faction, classType);
    if (!classInfo) errors.push("unknown_class_template");

    const filled = slots.filter(Boolean);

    if (filled.length > SLOT_COUNT) errors.push("too_many_slots");

    const skillNames = filled.map(s => s.skill);
    if (new Set(skillNames).size !== skillNames.length) errors.push("duplicate_skills");

    const fSkill = factionSkillName(data, faction);
    if (!slots[0] || slots[0].skill !== fSkill) warnings.push("faction_skill_not_in_center");

    for (const slot of filled) {
      if (classInfo && !isSkillAllowed(data, classInfo, slot.skill)) {
        errors.push("skill_not_allowed:" + slot.skill);
      }
      if (slot.tier >= 2 && !slot.advSub) warnings.push("missing_adv_sub:" + slot.skill);
      if (slot.tier >= 3 && !slot.expSub) warnings.push("missing_exp_sub:" + slot.skill);
    }

    if (targetSubclass && classInfo) {
      const prog = subclassProgress(data, classInfo, slots, targetSubclass);
      if (!prog.complete && filled.length >= SLOT_COUNT) {
        warnings.push("slots_full_subclass_incomplete");
      }
    }

    const startTiers = getConfiguratorStartingTiers(data, faction);
    const currentTiers = getCurrentSkillTiers(slots);
    const levelCost = computeBuildLevelCost(startTiers, currentTiers);
    if (!levelCost.slotsOk) errors.push("build_too_many_skills");
    if (!levelCost.levelOk) errors.push("build_level_too_high");

    return {
      ok: errors.length === 0,
      errors,
      warnings,
      levelCost,
      subclass: targetSubclass && classInfo
        ? subclassProgress(data, classInfo, slots, targetSubclass)
        : null
    };
  }

  /** Fill empty slots with allowed skills (for smoke tests). */
  function assembleMaxBuild(data, faction, classType, options = {}) {
    const slots = buildConfiguratorSlots(data, faction);
    const classInfo = findClassTemplate(data, faction, classType);
    const used = new Set(slots.filter(Boolean).map(s => s.skill));
    const targetSubclass = options.targetSubclass ?? null;
    const required = targetSubclass && classInfo
      ? getRequiredSkills(data, classInfo, targetSubclass)
      : [];

    const pickTier = skill => (required.includes(skill) ? 3 : 1);

    for (const skill of required) {
      if (used.has(skill)) {
        const slot = slots.find(s => s && s.skill === skill);
        if (slot && !slot.locked) slot.tier = 3;
        continue;
      }
      const idx = slots.findIndex(s => !s);
      if (idx < 0) break;
      const sk = data.skills[skill];
      slots[idx] = {
        skill,
        tier: pickTier(skill),
        advSub: sk?.adv?.[0] ?? null,
        expSub: sk?.exp?.[0] ?? null,
        locked: false
      };
      used.add(skill);
    }

    const extras = Object.keys(data.skills)
      .filter(name => !data.skills[name].faction)
      .filter(name => isSkillAllowed(data, classInfo, name))
      .filter(name => !used.has(name))
      .sort();

    for (const skill of extras) {
      const idx = slots.findIndex(s => !s);
      if (idx < 0) break;
      slots[idx] = { skill, tier: 1, advSub: null, expSub: null, locked: false };
      used.add(skill);
    }

    return { slots, targetSubclass };
  }

  return {
    SLOT_COUNT,
    MAX_PRACTICAL_LEVEL,
    normSkill,
    factionSkillName,
    findClassTemplate,
    buildConfiguratorSlots,
    getConfiguratorStartingTiers,
    isSkillAllowed,
    buildInitialSlots,
    usedSlotCount,
    getRequiredSkills,
    skillLevel,
    subclassProgress,
    hasSubskill,
    synergyStatus,
    computeSynergies,
    getStartingSkillTiers,
    getCurrentSkillTiers,
    computeBuildLevelCost,
    validateBuild,
    assembleMaxBuild
  };
});
