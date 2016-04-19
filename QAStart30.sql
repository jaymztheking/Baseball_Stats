select 
	g."GAME_KEY",
	g."GAME_DATE",
	g."GAME_TIME",
	a."TEAM_ABBREV",
	h."TEAM_ABBREV",
	p."INNING",
	p."SITUATION_KEY",
	p."END_SITUATION_KEY",
	p."PLAY_TYPE"

from "PITCH_RESULT" p
inner join "GAME" g on g."GAME_KEY" = p."GAME_KEY"
inner join "TEAM" h on h."TEAM_KEY" = g."HOME_TEAM_KEY"
inner join "TEAM" a on a."TEAM_KEY" = g."AWAY_TEAM_KEY"
where 
"SITUATION_KEY" = "END_SITUATION_KEY" 
and "PLAY_TYPE" not in ('No Play', 'Pinch Runner', 'Error on Foul') 
and "RBIS" = 0 
--and "SITUATION_KEY" = 30;
and "SITUATION_KEY" = "END_SITUATION_KEY";

select * from "PITCH_RESULT" where "GAME_KEY" = 440 and "INNING" = 'Bot 6' order by "PLAY_NUM"