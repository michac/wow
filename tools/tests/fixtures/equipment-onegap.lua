-- Fixture: a mostly-Hero char with ONE real gap — waist 246 (a leftover Champion
-- piece), everything else 259–269. Purpose-built for the Phase-3 EV test: a
-- targeted vendor buy (Maren) can close the waist gap deterministically, while a
-- random [all] roll usually lands on an already-good slot. finger2/neck/feet/
-- hands/trinket2 sit exactly at 259 so a Hero-259 landing is a sidegrade there —
-- only waist (246) is a sub-259 upgrade, which makes the random-vs-targeted gap
-- sharp and the expected-delta math exact (one sub-259 slot).
PlannerStateDB = {
["character"] = "Onegap",
["realm"] = "Kil'jaeden",
["schema"] = 4,
["equippedIlvl"] = 261,
["equipment"] = {
{ ["slot"] = "head",     ["ilvl"] = 266, },
{ ["slot"] = "neck",     ["ilvl"] = 259, },
{ ["slot"] = "shoulder", ["ilvl"] = 266, },
{ ["slot"] = "chest",    ["ilvl"] = 263, },
{ ["slot"] = "waist",    ["ilvl"] = 246, },
{ ["slot"] = "legs",     ["ilvl"] = 263, },
{ ["slot"] = "feet",     ["ilvl"] = 259, },
{ ["slot"] = "wrist",    ["ilvl"] = 266, },
{ ["slot"] = "hands",    ["ilvl"] = 259, },
{ ["slot"] = "back",     ["ilvl"] = 266, },
{ ["slot"] = "finger1",  ["ilvl"] = 263, },
{ ["slot"] = "finger2",  ["ilvl"] = 259, },
{ ["slot"] = "trinket1", ["ilvl"] = 266, },
{ ["slot"] = "trinket2", ["ilvl"] = 259, },
{ ["slot"] = "mainhand", ["ilvl"] = 269, },
{ ["slot"] = "offhand",  ["ilvl"] = 269, },
},
["currencies"] = { },
["vault"] = { ["hasRewards"] = false, ["slots"] = { }, },
["mythicPlus"] = { },
["weeklyQuests"] = { },
["lockouts"] = { },
}
