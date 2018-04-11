-- Table: public.play

-- DROP TABLE public.play;

CREATE TABLE public.play
(
    game_key integer NOT NULL,
    play_seq_no smallint NOT NULL,
    hitter_key integer NOT NULL,
    pitcher_key integer NOT NULL,
    top_bot_inn smallint,
    inning_num smallint,
    pitch_seq character varying(30) COLLATE pg_catalog."default",
    play_seq character varying(30) COLLATE pg_catalog."default",
    play_type character varying(20) COLLATE pg_catalog."default",
    plate_app boolean,
    at_bat boolean,
    hit boolean,
    strikes smallint,
    balls smallint,
    contact_x smallint,
    swing_x smallint,
    look_x smallint,
    ball_loc character varying(10) COLLATE pg_catalog."default",
    ball_type character varying(20) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.play
    OWNER to babypng;

GRANT ALL ON TABLE public.play TO babypng;

GRANT INSERT, SELECT, UPDATE, REFERENCES, TRIGGER ON TABLE public.play TO py;