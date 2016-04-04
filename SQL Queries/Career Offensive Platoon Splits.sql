﻿with sums as (
select  "HITTER_KEY",
	p."THROW_HAND",
	sum(bb) as bb,
	sum(ibb) as ibb,
	sum(hbp) as hbp,
	sum(single) as single,
	sum(double) as double,
	sum(triple) as triple,
	sum(hr) as hr,
	sum(ab) as ab,
	sum(sf) as sf,
	sum(k) as k
from "AB_STATS" a
inner join "GAME" g on g."GAME_KEY" = a."GAME_KEY"
inner join "PITCHER_STATS" p on p."PLAYER_KEY" = a."PITCHER_KEY"
group by "HITTER_KEY","THROW_HAND" having sum(ab) > 0)

select sums."HITTER_KEY",
"NAME",
"THROW_HAND",
ab,
case when (ab+bb-ibb+sf+hbp) = 0 Then 0 else (.687*(bb-ibb)+.718*hbp+.881*single+1.256*double+1.594*triple+2.065*hr)/(ab+bb-ibb+sf+hbp) end as woba,
case when (ab-k-hr+sf) = 0 Then 0 else (single+double+triple)/((ab-k-hr+sf)*1.0) end as BABIP,
(double + 2*triple + 3*hr)/(ab*1.0) as iso

from sums
inner join "HITTER_STATS" on sums."HITTER_KEY"= "HITTER_STATS"."PLAYER_KEY"
where sums."HITTER_KEY" = 140
;
