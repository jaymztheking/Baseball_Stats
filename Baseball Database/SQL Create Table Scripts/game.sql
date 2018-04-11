-- Table: public.game

-- DROP TABLE public.game;

CREATE TABLE public.game
(
    game_key serial NOT NULL,
    game_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    game_date date NOT NULL,
    game_time time without time zone NOT NULL,
    home_team_key smallint NOT NULL,
    away_team_key smallint NOT NULL,
    park_key smallint,
    game_temp_f real,
    wind_dir character varying(20) COLLATE pg_catalog."default",
    field_condition character varying(20) COLLATE pg_catalog."default",
    precipitation character varying(20) COLLATE pg_catalog."default",
    sky_cond character varying(20) COLLATE pg_catalog."default",
    total_innings smallint,
    home_hits smallint,
    away_hits smallint,
    home_runs smallint,
    away_runs smallint,
    home_team_win boolean,
    tie boolean,
    game_time_minutes smallint,
    home_ump_id character varying(20) COLLATE pg_catalog."default",
    attendance integer,
    CONSTRAINT game_pk_game_key PRIMARY KEY (game_key),
    CONSTRAINT game_fk_away_team_key FOREIGN KEY (away_team_key)
        REFERENCES public.team (team_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT game_fk_home_team_key FOREIGN KEY (home_team_key)
        REFERENCES public.team (team_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT game_fk_park_key FOREIGN KEY (park_key)
        REFERENCES public.park (park_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.game
    OWNER to babypng;

GRANT ALL ON TABLE public.game TO babypng;

GRANT INSERT, SELECT, UPDATE, REFERENCES, TRIGGER ON TABLE public.game TO py;