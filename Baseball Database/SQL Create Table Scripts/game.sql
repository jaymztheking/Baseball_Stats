-- Table: public.game

-- DROP TABLE public.game;

CREATE TABLE public.game
(
    game_key integer NOT NULL DEFAULT nextval('game_game_key_seq'::regclass),
    park_key integer NOT NULL,
    game_date date NOT NULL,
    game_time time without time zone NOT NULL,
    home_team_key integer NOT NULL,
    away_team_key integer NOT NULL,
    wind_dir character varying(15) COLLATE pg_catalog."default",
    wind_speed_mph smallint,
    weather_condition character varying(30) COLLATE pg_catalog."default",
    total_innings smallint,
    home_hits smallint,
    away_hits smallint,
    home_runs smallint,
    away_runs smallint,
    game_temp_f smallint,
    "home_team_win?" boolean,
    "tie?" boolean,
    game_time_minutes smallint,
    home_ump_id character varying(15) COLLATE pg_catalog."default",
    CONSTRAINT game_pkey PRIMARY KEY (game_key),
    CONSTRAINT away_team_fkey FOREIGN KEY (away_team_key)
        REFERENCES public.team (team_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT home_team_fkey FOREIGN KEY (home_team_key)
        REFERENCES public.team (team_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT park_fkey FOREIGN KEY (park_key)
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

GRANT ALL ON TABLE public.game TO py;