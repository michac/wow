-- Fixture: a fresh level-90 (Encomplete-ish early), low ilvl across slots.
-- A Hero-ceiling activity (reward_ilvl_max ~279) is a big upgrade here -> high R.
-- schema>=4 carries per-slot equipment ilvls (plan.py weakest_slots / slot_target_R).
PlannerStateDB = {
["character"] = "FixtureFresh",
["realm"] = "Kil'jaeden",
["schema"] = 4,
["equippedIlvl"] = 214,
["equipment"] = {
{ ["slot"] = "HEAD",     ["ilvl"] = 220, },
{ ["slot"] = "NECK",     ["ilvl"] = 210, },
{ ["slot"] = "SHOULDER", ["ilvl"] = 216, },
{ ["slot"] = "CHEST",    ["ilvl"] = 218, },
{ ["slot"] = "WAIST",    ["ilvl"] = 210, },
{ ["slot"] = "LEGS",     ["ilvl"] = 220, },
{ ["slot"] = "FEET",     ["ilvl"] = 212, },
{ ["slot"] = "WRIST",    ["ilvl"] = 205, },
{ ["slot"] = "HANDS",    ["ilvl"] = 208, },
{ ["slot"] = "BACK",     ["ilvl"] = 200, },
{ ["slot"] = "FINGER_1", ["ilvl"] = 215, },
{ ["slot"] = "FINGER_2", ["ilvl"] = 213, },
},
["vault"] = { ["hasRewards"] = false, ["slots"] = { }, },
["mythicPlus"] = { },
["weeklyQuests"] = { },
["lockouts"] = { },
}
