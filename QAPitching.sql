select  
	sum(case when "WIN?" then 1 else 0 end) as wins,
	sum(case when "LOSS?" then 1 else 0 end) as losses,
	sum(case when "COMPLETE_GAME?" then 1 else 0 end) as cg,
	sum(case when "SHUT_OUT?" then 1 else 0 end) as so,
	sum(case when "SAVE?" then 1 else 0 end) as sv,
	sum("IP") as IP,
	sum("HITS") as hits,
	sum("EARNED_RUNS") as er,
	sum("BB") as bb,
	sum("K") as k,
	sum("HBP") as hbp
from "PITCH_ROSTER" where "PITCHER_KEY" = 192