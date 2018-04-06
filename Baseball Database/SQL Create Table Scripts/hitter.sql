-- Table: public.hitter

-- DROP TABLE public.hitter;

CREATE TABLE public.hitter
(
    player_key serial NOT NULL,
    name character varying(100) COLLATE pg_catalog."default",
    height_inch double precision,
    weight_lbs double precision,
    birth_date date,
    mlb_debut_date date,
    bat_hand character varying(1) COLLATE pg_catalog."default",
    rs_user_id character varying(20) COLLATE pg_catalog."default",
    br_user_id character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT hitter_pkey PRIMARY KEY (player_key)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.hitter
    OWNER to babypng;

GRANT ALL ON TABLE public.hitter TO babypng;

GRANT ALL ON TABLE public.hitter TO py;