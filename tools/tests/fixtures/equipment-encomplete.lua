-- Fixture: Encomplete's REAL per-slot ilvls (Kil'jaeden main, 12.0.7, dumped
-- 2026-07-07 — see knowledge/characters/encomplete-kiljaeden.md). A geared main:
-- weakest slots waist/finger2/trinket2 all 259, most 276, back/mainhand 285.
-- A Hero drop LANDS at 259 (dawncrests.md 1/6), so it's a sidegrade to his 259
-- slots -> slot_target_R = 0 for every migrated drop activity (Phase 2a headline).
-- His upgrades come from crests (Myth = bottleneck), not new drops.
-- Real slot-name casing from the live dump: lowercase (waist/finger2/mainhand/…).
PlannerStateDB = {
["character"] = "Encomplete",
["realm"] = "Kil'jaeden",
["schema"] = 4,
["equippedIlvl"] = 272.4375,
["equipment"] = {
{ ["slot"] = "head",     ["ilvl"] = 276, },
{ ["slot"] = "neck",     ["ilvl"] = 263, },
{ ["slot"] = "shoulder", ["ilvl"] = 276, },
{ ["slot"] = "chest",    ["ilvl"] = 276, },
{ ["slot"] = "waist",    ["ilvl"] = 259, },
{ ["slot"] = "legs",     ["ilvl"] = 276, },
{ ["slot"] = "feet",     ["ilvl"] = 276, },
{ ["slot"] = "wrist",    ["ilvl"] = 266, },
{ ["slot"] = "hands",    ["ilvl"] = 276, },
{ ["slot"] = "back",     ["ilvl"] = 285, },
{ ["slot"] = "finger1",  ["ilvl"] = 266, },
{ ["slot"] = "finger2",  ["ilvl"] = 259, },
{ ["slot"] = "trinket1", ["ilvl"] = 276, },
{ ["slot"] = "trinket2", ["ilvl"] = 259, },
{ ["slot"] = "mainhand", ["ilvl"] = 285, },
},
["currencies"] = {
{ ["name"] = "Hero Dawncrest",  ["quantity"] = 176, },
{ ["name"] = "Myth Dawncrest",  ["quantity"] = 20, },
{ ["name"] = "Field Accolade",  ["quantity"] = 1309, },
},
["vault"] = { ["hasRewards"] = false, ["slots"] = { }, },
["mythicPlus"] = { },
["weeklyQuests"] = { },
["lockouts"] = { },
}
