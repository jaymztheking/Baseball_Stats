select
	g."GAME_KEY",
	g."GAME_DATE",
	res."HITTER_KEY",
	case when l."TEAM_KEY" = g."HOME_TEAM_KEY" then 'HOME' else 'AWAY' end as "HOME_AWAY",
	case when l."TEAM_KEY" = g."HOME_TEAM_KEY" then hsp."THROW_HAND" else asp."THROW_HAND" end as "START_PITCH_HAND",
	p."THROW_HAND" as "CURRENT_PITCH_HAND",
	case when res."PLAY_TYPE" = 'Hit By Pitch' then 1 else 0 end as "HBP",
	case when res."PLAY_TYPE" = 'Single' then 1 else 0 end as "SINGLE",
	case when res."PLAY_TYPE" in ('Double','Ground Rule Double') then 1 else 0 end as "DOUBLE",
	case when res."PLAY_TYPE" = 'Triple' then 1 else 0 end as "TRIPLE",
	case when res."PLAY_TYPE" = 'Home Run' then 1 else 0 end as "HR",
	case when res."PLAY_TYPE" = 'Walk' then 1 else 0 end as "BB",
	case when (res."PLAY_TYPE" = 'Walk' and res."PITCH_SEQUENCE" LIKE '%I') then 1 else 0 end as "IBB",
	case when res."PLAY_TYPE" like 'Sac%' then 1 else 0 end as "SF",
	case when res."PLAY_TYPE" = 'Strikeout' then 1 else 0 end as "K",
	case when res."PLAY_TYPE" in ('Strikeout', 'Out','Reach on Error','Lineout','Double','Ground Rule Double','Flyout','Triple','FC','Groundout','Single','Home Run','GDP') then 1 else 0 end as "AB"
from "GAME" g
inner join "PITCH_RESULT" res on res."GAME_KEY" = g."GAME_KEY"
inner join "LINEUP" l on l."PLAYER_KEY" = res."HITTER_KEY" and l."GAME_KEY" = res."GAME_KEY"
inner join (select * from "PITCH_ROSTER" where "PITCHER_ROLE" = 'Starter')hros on hros."GAME_KEY" = g."GAME_KEY" and g."HOME_TEAM_KEY" = hros."TEAM_KEY"
inner join "PITCHER_STATS" hsp on hsp."PLAYER_KEY" = hros."PITCHER_KEY"
inner join (select * from "PITCH_ROSTER" where "PITCHER_ROLE" = 'Starter')aros on aros."GAME_KEY" = g."GAME_KEY" and g."HOME_TEAM_KEY" = aros."TEAM_KEY"
inner join "PITCHER_STATS" asp on asp."PLAYER_KEY" = aros."PITCHER_KEY"
inner join "PITCHER_STATS" p on p."PLAYER_KEY" = res."PITCHER_KEY"
