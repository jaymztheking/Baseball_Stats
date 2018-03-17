-- Table: public.play

-- DROP TABLE public.play;

CREATE TABLE public.play
(
    game_key integer NOT NULL,
    hitter_key integer NOT NULL,
    pitcher_key integer NOT NULL,
    play_seq_no smallint NOT NULL,
    start_sit smallint,
    end_sit smallint,
    inning character varying(10) COLLATE pg_catalog."default",
    pitch_seq character varying(25) COLLATE pg_catalog."default",
    strikes smallint,
    balls smallint,
    contact_x smallint,
    swing_x smallint,
    look_x smallint,
    play_type character varying(25) COLLATE pg_catalog."default",
    "hit?" boolean,
    result_outs smallint,
    ball_loc character varying(10) COLLATE pg_catalog."default",
    ball_type character varying(25) COLLATE pg_catalog."default",
    "batter_scored?" boolean,
    runs_in smallint,
    "at_bat?" boolean,
    "plate_app?" boolean,
    CONSTRAINT game_fkey FOREIGN KEY (game_key)
        REFERENCES public.game (game_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT hitter_fkey FOREIGN KEY (hitter_key)
        REFERENCES public.hitter (player_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT pitcher_fkey FOREIGN KEY (pitcher_key)
        REFERENCES public.pitcher (player_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.play
    OWNER to babypng;

GRANT ALL ON TABLE public.play TO babypng;

GRANT ALL ON TABLE public.play TO py;