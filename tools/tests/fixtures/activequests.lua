-- Schema-6 fixture: a PlannerState dump carrying the activeQuests[] block emitted
-- by scanQuestLog() (the full accepted-quest log, added in addon v0.5.0). Drives
-- wowkb.plan.discover_weeklies: a weekly-frequency quest present here but absent
-- from the watchlist (weeklyQuests) is "discovered". frequency: 0 default / 1 daily
-- / 2 weekly. Here 96713 is weekly AND already watch-listed (skip); 99001 is a
-- weekly not on the watchlist (discover); 99002 daily and 99003 default (ignore).
PlannerStateDB = {
["character"] = "Uncomplete",
["realm"] = "Kil'jaeden",
["schema"] = 6,
["weeklyQuests"] = {
{ ["id"] = 94446, ["label"] = "prey_weekly", ["complete"] = false },
{ ["id"] = 96713, ["label"] = "Showdown on Val", ["complete"] = false },
},
["activeQuests"] = {
{ ["id"] = 96713, ["title"] = "Showdown on Val", ["frequency"] = 2 },
{ ["id"] = 99001, ["title"] = "Knocking Off the Top", ["frequency"] = 2, ["campaign"] = 1 },
{ ["id"] = 99002, ["title"] = "A Daily Bounty", ["frequency"] = 1 },
{ ["id"] = 99003, ["title"] = "A One-Time Quest", ["frequency"] = 0 },
},
}
