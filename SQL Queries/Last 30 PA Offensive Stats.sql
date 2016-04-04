with lastThirty as (
select * from (
select p."HITTER_KEY", p."GAME_KEY", p."HITTER_PA", rank() over (PARTITION BY p."HITTER_KEY" ORDER BY g."GAME_DATE" DESC, g."GAME_TIME" DESC, p."HITTER_PA" DESC) as "PLATE"   
from "PITCH_RESULT" p
inner join "GAME" g on p."GAME_KEY" = g."GAME_KEY") bubba
where "PLATE" <= 30
)

, sums as (
select  a."HITTER_KEY",
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
inner join lastThirty t on t."HITTER_KEY" = a."HITTER_KEY" and t."GAME_KEY" = a."GAME_KEY" and t."HITTER_PA" = a."HITTER_PA"
group by a."HITTER_KEY" having sum(ab) > 0)

select sums."HITTER_KEY",
"NAME",
ab,
case when (ab+bb-ibb+sf+hbp) = 0 Then 0 else (.687*(bb-ibb)+.718*hbp+.881*single+1.256*double+1.594*triple+2.065*hr)/(ab+bb-ibb+sf+hbp) end as woba,
case when (ab-k-hr+sf) = 0 Then 0 else (single+double+triple)/((ab-k-hr+sf)*1.0) end as BABIP,
(double + 2*triple + 3*hr)/(ab*1.0) as iso

from sums
inner join "HITTER_STATS" on sums."HITTER_KEY"= "HITTER_STATS"."PLAYER_KEY"
where sums."HITTER_KEY" = 140
;
