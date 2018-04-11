-- Table: public.base

-- DROP TABLE public.base;

CREATE TABLE public.base
(
    game_key integer NOT NULL,
    play_seq_no smallint NOT NULL,
    run_seq character varying(20) COLLATE pg_catalog."default",
    top_bot_inn smallint,
    inning_num smallint,
    start_outs smallint,
    end_outs smallint,
    start_first character varying(10) COLLATE pg_catalog."default",
    start_second character varying(10) COLLATE pg_catalog."default",
    start_third character varying(10) COLLATE pg_catalog."default",
    end_first character varying(10) COLLATE pg_catalog."default",
    end_second character varying(10) COLLATE pg_catalog."default",
    end_third character varying(10) COLLATE pg_catalog."default",
    second_stolen boolean,
    third_stolen boolean,
    home_stolen boolean,
    total_sb smallint,
    second_caught boolean,
    third_caught boolean,
    home_caught boolean,
    total_cs smallint,
    batter_scored boolean,
    first_scored boolean,
    second_scored boolean,
    third_scored boolean,
    total_runs smallint,
    rbi smallint,
    CONSTRAINT base_fk_game_key FOREIGN KEY (game_key)
        REFERENCES public.game (game_key) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.base
    OWNER to babypng;

GRANT ALL ON TABLE public.base TO babypng;

GRANT INSERT, SELECT, UPDATE, REFERENCES, TRIGGER ON TABLE public.base TO py;