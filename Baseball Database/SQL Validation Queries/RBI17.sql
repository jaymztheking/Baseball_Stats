select
    g.game_date,
    g.game_key,
    sum(d.rbi)
from hitdims d
inner join team t on d.team_key = t.team_key
inner join game g on g.game_key = d.game_key
where
	extract(year from g.game_date) = 2017
    and t.team_abbrev_br = 'ARI'
group by
	g.game_date,
    g.game_time,
    g.game_key
order by
	g.game_date,
    g.game_time,
    g.game_key