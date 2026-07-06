-- Schema-3 fixture: a PlannerState dump carrying the worldBosses[] block emitted
-- by scanWorldBosses() (GetSavedWorldBossInfo). The WoW API lists ONLY bosses
-- already killed this reset, so a non-empty block == the weekly world-boss lockout
-- is done. Drives wowkb.plan's world_boss_weekly gate -> "done" (Lua parse -> gate).
PlannerStateDB = {
["character"] = "Encomplete",
["realm"] = "Kil'jaeden",
["schema"] = 3,
["worldBosses"] = {
{ ["name"] = "Imperator Pertinax", ["id"] = 1 },
},
["vault"] = {
["hasRewards"] = false,
["slots"] = {
},
},
["weeklyQuests"] = {
},
["lockouts"] = {
},
}
