-- Calendar fixture: a schema-2 dump with a LIVE Timewalking event, driving the
-- event_active "fun radar" gate end-to-end. Expectations via wowkb.plan:
--   timewalking-event (match "Timewalking") -> gate todo (live) -> surfaces, no (?)
--   an inactive event in the same block must NOT trigger it.
PlannerStateDB = {
["character"] = "Encomplete",
["schema"] = 2,
["vault"] = { ["hasRewards"] = false, ["slots"] = {}, },
["mythicPlus"] = {
},
["weeklyQuests"] = {
},
["lockouts"] = {
},
["calendar"] = {
{ ["title"] = "Timewalking Dungeon Event", ["active"] = true,  ["startTime"] = "2026-06-30", ["endTime"] = "2026-08-11", },
{ ["title"] = "Darkmoon Faire",            ["active"] = true,  ["startTime"] = "2026-07-05", ["endTime"] = "2026-08-08", },
{ ["title"] = "Arena Skirmish Bonus Event",["active"] = false, ["startTime"] = "2026-07-28", ["endTime"] = "2026-08-04", },
},
}
