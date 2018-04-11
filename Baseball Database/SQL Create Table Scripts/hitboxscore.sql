-- Table: public.hitboxscore

-- DROP TABLE public.hitboxscore;

CREATE TABLE public.hitboxscore
(
    game_key integer NOT NULL,
    team_key smallint NOT NULL,
    player_key integer NOT NULL,
    batting_num smallint,
    "position" character varying(5) COLLATE pg_catalog."default",
    plate_app smallint,
    at_bat smallint,
    so smallint,
    hits smallint,
    bb smallint,
    ibb smallint,
    hbp smallint,
    runs smallint,
    rbi smallint,
    single smallint,
    double smallint,
    triple smallint,
    hr smallint,
    sb smallint,
    cs smallint,
    CONSTRAINT hitboxscore_fk_game_key FOREIGN KEY (game_key)
        REFERENCES public.game (game_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT hitboxscore_fk_player_key FOREIGN KEY (player_key)
        REFERENCES public.hitter (player_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT hitboxscore_fk_team_key FOREIGN KEY (team_key)
        REFERENCES public.team (team_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.hitboxscore
    OWNER to babypng;

GRANT ALL ON TABLE public.hitboxscore TO babypng;

GRANT INSERT, SELECT, UPDATE, REFERENCES, TRIGGER ON TABLE public.hitboxscore TO py;