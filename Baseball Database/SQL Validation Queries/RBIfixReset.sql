update play set rbis_in = 0
;
update play set rbis_in = runs_in
where
	play_type in 
    ('Interference','Walk','Hit By Pitch','Sacrifice Fly','Sacrifice Hit','Out','Fielders Choice','Single','Double','Ground Rule Double','Triple','Home Run');
;
commit;