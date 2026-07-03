-- Fixture: mid-track M+ vault progress (2 runs this week).
-- n=2 -> next run reaches 3, NOT a threshold (1/4/8) -> mplus-vault keeps its flat
-- reward_base (R=3, no breakpoint boost). Real SavedVariables ["key"]=value format.
PlannerStateDB = {
["character"] = "FixtureBelow",
["realm"] = "Kil'jaeden",
["schema"] = 1,
["vault"] = {
["hasRewards"] = false,
["slots"] = {
},
},
["mythicPlus"] = {
{ ["thisWeek"] = true, ["level"] = 10, ["completed"] = true, },
{ ["thisWeek"] = true, ["level"] = 10, ["completed"] = true, },
},
["weeklyQuests"] = {
},
["lockouts"] = {
},
}
