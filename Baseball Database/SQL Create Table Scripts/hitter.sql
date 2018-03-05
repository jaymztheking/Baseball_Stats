-- Table: public.hitters

-- DROP TABLE public.hitters;

CREATE TABLE public.hitters
(
    player_key integer NOT NULL,
    name character varying(100) COLLATE pg_catalog."default",
    height_inch float8,
    weight_lbs float8,
    birth_date date,
    mlb_debut_date date,
    bat_hand character varying(1) COLLATE pg_catalog."default",
    rs_user_id character varying(20) COLLATE pg_catalog."default",
    br_user_id character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT hitters_pkey PRIMARY KEY (player_key)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.hitters
    OWNER to babypng;