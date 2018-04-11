-- Table: public.hitter

-- DROP TABLE public.hitter;

CREATE TABLE public.hitter
(
    player_key serial NOT NULL,
    name character varying(30) COLLATE pg_catalog."default",
    height_inch real,
    weight_lbs real,
    birth_date date,
    mlb_debut_date date,
    bat_hand character varying(5) COLLATE pg_catalog."default",
    throw_hand character varying(5) COLLATE pg_catalog."default",
    rs_user_id character varying(10) COLLATE pg_catalog."default",
    br_user_id character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT hitter_pk_player_key PRIMARY KEY (player_key)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.hitter
    OWNER to babypng;

GRANT ALL ON TABLE public.hitter TO babypng;

GRANT INSERT, SELECT, UPDATE, REFERENCES, TRIGGER ON TABLE public.hitter TO py;