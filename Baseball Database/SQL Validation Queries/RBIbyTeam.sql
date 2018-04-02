select 
	t.team_abbrev_br,
    sum(d.rbi)
from hitdims d
inner join team t on d.team_key = t.team_key
inner join game g on g.game_key = d.game_key
where
	extract(year from g.game_date) = 2017
group by
	t.team_abbrev_br