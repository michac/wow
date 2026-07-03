-- Fixture: M+ vault progress sitting right below a threshold (3 runs this week).
-- n=3 -> next run reaches 4, a threshold -> mplus-vault R boosted to 4, row shows
-- "next run unlocks vault slot 2". Gate (mplus_weekly_lt n=8) still todo, so it
-- survives into scoring and should rank ABOVE its vault-below score.
PlannerStateDB = {
["character"] = "FixtureCrossing",
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
{ ["thisWeek"] = true, ["level"] = 10, ["completed"] = true, },
},
["weeklyQuests"] = {
},
["lockouts"] = {
},
}
