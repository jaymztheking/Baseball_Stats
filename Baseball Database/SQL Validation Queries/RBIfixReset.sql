update play set rbis_in = 0
;
commit;
;
update play set rbis_in = runs_in
where
	play_type in 
    ('Interference','Walk','Hit By Pitch','Sacrifice Fly','Sacrifice Hit','Out','Fielders Choice','Single','Double','Ground Rule Double','Triple','Home Run');
commit;
update play set rbis_in = runs_in
where
	play_type = 'Reach On Error'
    and start_sit in (4,5,6,7,14,15,16,17)
;
commit;