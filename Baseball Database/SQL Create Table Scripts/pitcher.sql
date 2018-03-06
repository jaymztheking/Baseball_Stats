-- Table: public.pitcher

-- DROP TABLE public.pitcher;

CREATE TABLE public.pitcher
(
    player_key serial NOT NULL,
    name character varying(100) COLLATE pg_catalog."default",
    height_inch double precision,
    weight_lbs double precision,
    birth_date date,
    mlb_debut_date date,
    throw_hand character varying(1) COLLATE pg_catalog."default",
    rs_user_id character varying(20) COLLATE pg_catalog."default",
    br_user_id character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT pitcher_pkey PRIMARY KEY (player_key)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.pitcher
    OWNER to babypng;

GRANT ALL ON TABLE public.pitcher TO babypng;

GRANT ALL ON TABLE public.pitcher TO py;