-- Table: public.pitchboxscore

-- DROP TABLE public.pitchboxscore;

CREATE TABLE public.pitchboxscore
(
    game_key integer NOT NULL,
    team_key integer NOT NULL,
    player_key integer NOT NULL,
    pitch_role character varying(10) COLLATE pg_catalog."default" NOT NULL,
    pitch_count smallint,
    "K" smallint,
    "BB" smallint,
    "IBB" smallint,
    "HBP" smallint,
    hits smallint,
    earned_runs smallint,
    "IP" real,
    strikes smallint,
    balls smallint,
    complete_game boolean,
    shut_out boolean,
    no_hitter boolean,
    win boolean,
    loss boolean,
    save boolean,
    swing_strikes smallint,
    look_strikes smallint,
    contact_strikes smallint,
    flyballs smallint,
    groundballs smallint,
    line_drives smallint,
    CONSTRAINT pitchboxscore_fk_game_key FOREIGN KEY (game_key)
        REFERENCES public.game (game_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT pitchboxscore_fk_player_key FOREIGN KEY (game_key)
        REFERENCES public.pitcher (player_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT pitchboxscore_fk_team_key FOREIGN KEY (team_key)
        REFERENCES public.team (team_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.pitchboxscore
    OWNER to babypng;

GRANT ALL ON TABLE public.pitchboxscore TO babypng;

GRANT INSERT, SELECT, UPDATE, REFERENCES, TRIGGER ON TABLE public.pitchboxscore TO py;