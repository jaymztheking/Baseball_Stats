select 
h."NAME",
l."PLAYER_POS",
l."AT_BATS",
l."RUNS",
1."HITS",
l."RBI",
l."BB",
'X' as "K",
l."PA"
from "LINEUP" l
inner join "HITTER_STATS" h on l."PLAYER_KEY" = h."PLAYER_KEY"
order by "TEAM_KEY", "PLAYER_BAT_NUM"