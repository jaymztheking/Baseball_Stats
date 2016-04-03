﻿select 

	sum("AT_BATS"),
	sum("RUNS"),
	sum("HITS"),
	sum("2B"),
	sum("3B"),
	sum("HR"),
	sum("RBI"),
	sum("BB"),
	sum("SB"),
	sum("CS")
from "LINEUP" l
inner join "GAME" g on l."GAME_KEY" = g."GAME_KEY"
where 
l."PLAYER_KEY" = 140 
and g."GAME_DATE" > '2015-01-01'