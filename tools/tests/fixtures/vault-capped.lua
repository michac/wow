-- Fixture: M+ vault fully capped (8 runs this week).
-- The mplus_weekly_lt gate (n=8) resolves to DONE and drops mplus-vault from the
-- plan entirely (vault M+ column maxed). breakpoint_R would independently return
-- R=0 here; the gate just gets there first for this candidate.
PlannerStateDB = {
["character"] = "FixtureCapped",
["realm"] = "Kil'jaeden",
["schema"] = 1,
["vault"] = {
["hasRewards"] = false,
["slots"] = {
},
},
["mythicPlus"] = {
{ ["thisWeek"] = true, }, { ["thisWeek"] = true, }, { ["thisWeek"] = true, },
{ ["thisWeek"] = true, }, { ["thisWeek"] = true, }, { ["thisWeek"] = true, },
{ ["thisWeek"] = true, }, { ["thisWeek"] = true, },
},
["weeklyQuests"] = {
},
["lockouts"] = {
},
}
