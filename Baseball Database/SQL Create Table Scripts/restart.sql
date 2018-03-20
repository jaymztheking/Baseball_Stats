truncate hitboxscore, pitchboxscore, play, game, pitcher, hitter CASCADE ;
alter sequence pitcher_player_key_seq restart with 1;
alter sequence hitter_player_key_seq restart with 1;
alter sequence game_game_key_seq restart with 1;