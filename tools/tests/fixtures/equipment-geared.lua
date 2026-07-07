-- Fixture: a Hero-capped main — every slot at 279 (Hero 6/6). A Hero-ceiling
-- activity (reward_ilvl_max ~279) can no longer upgrade any slot -> R≈0, so
-- world-vault / voidcore / prey-map sources correctly fall down the list.
PlannerStateDB = {
["character"] = "FixtureGeared",
["realm"] = "Kil'jaeden",
["schema"] = 4,
["equippedIlvl"] = 279,
["equipment"] = {
{ ["slot"] = "HEAD",     ["ilvl"] = 279, },
{ ["slot"] = "NECK",     ["ilvl"] = 279, },
{ ["slot"] = "SHOULDER", ["ilvl"] = 279, },
{ ["slot"] = "CHEST",    ["ilvl"] = 279, },
{ ["slot"] = "WAIST",    ["ilvl"] = 279, },
{ ["slot"] = "LEGS",     ["ilvl"] = 279, },
{ ["slot"] = "FEET",     ["ilvl"] = 279, },
{ ["slot"] = "WRIST",    ["ilvl"] = 279, },
{ ["slot"] = "HANDS",    ["ilvl"] = 279, },
{ ["slot"] = "BACK",     ["ilvl"] = 279, },
{ ["slot"] = "FINGER_1", ["ilvl"] = 279, },
{ ["slot"] = "FINGER_2", ["ilvl"] = 279, },
},
["vault"] = { ["hasRewards"] = false, ["slots"] = { }, },
["mythicPlus"] = { },
["weeklyQuests"] = { },
["lockouts"] = { },
}
