
delete from play
where game_key in (select game_key from game where home_team_key in (select team_key from team where team_abbrev_rs in('SEA','TBA')))
;
delete from hitboxscore
where game_key in (select game_key from game where home_team_key in (select team_key from team where team_abbrev_rs in('SEA','TBA')))
;
delete from pitchboxscore
where game_key in (select game_key from game where home_team_key in (select team_key from team where team_abbrev_rs in('SEA','TBA')))
;
delete from game
where home_team_key in (select team_key from team where team_abbrev_rs in('SEA','TBA'))
;
commit;