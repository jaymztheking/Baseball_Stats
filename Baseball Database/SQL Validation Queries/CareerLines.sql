select
	extract(year from g.game_date) season,
	h.name,
    sum(case when p.plate_app = True then 1 else 0 end) PA,
    sum(case when p.at_bat = True then 1 else 0 end) AB,
    sum(case when p.batter_scored = True then 1 else 0 end) R,
    sum(case when p.hit = True then 1 else 0 end) H,
    sum(case when p.play_type = 'Double' then 1 else 0 end) x2B,
    sum(case when p.play_type = 'Triple' then 1 else 0 end) x3B
from
	hitter h
inner join play p on p.hitter_key = h.player_key
inner join game g on g.game_key = p.game_key
where
	(g.home_team_key = 2 or g.away_team_key = 2)
group by
	extract(year from g.game_date),
	h.name
having
	sum(
        case
        when p.plate_app = True then 1
    	else 0 end) > 150