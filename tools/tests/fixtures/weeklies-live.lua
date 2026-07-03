-- Capstone fixture: what the addon emits once ns.WEEKLY_QUESTS is wired, driving
-- the FULL pipeline (Lua parse -> gate -> breakpoint score -> plan). Mirrors real
-- SavedVariables ["key"]=value format. Expectations when run through wowkb.plan:
--   prey_weekly (94446 complete)      -> gate done  -> drops from the plan
--   void_assault (94385 done/94386 not) -> gate done -> drops (any-of-pair rule)
--   mplus-vault (3 M+ this week)       -> breakpoint R=4, "next run unlocks vault slot 2"
--   delve/liadrin/dungeon/housing      -> still (?) (deliberately unconfigured)
PlannerStateDB = {
["character"] = "Encomplete",
["realm"] = "Kil'jaeden",
["schema"] = 1,
["vault"] = {
["hasRewards"] = false,
["slots"] = {
},
},
["mythicPlus"] = {
{ ["thisWeek"] = true, ["level"] = 10, }, { ["thisWeek"] = true, ["level"] = 10, },
{ ["thisWeek"] = true, ["level"] = 10, },
},
["weeklyQuests"] = {
{ ["id"] = 94446, ["label"] = "prey_weekly", ["complete"] = true, },
{ ["id"] = 94385, ["label"] = "void_assault", ["complete"] = true, },
{ ["id"] = 94386, ["label"] = "void_assault", ["complete"] = false, },
},
["lockouts"] = {
},
}
