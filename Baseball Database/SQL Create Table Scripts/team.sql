-- Table: public.team

-- DROP TABLE public.team;

CREATE TABLE public.team
(
    team_key integer NOT NULL,
    team_locale character varying(50) COLLATE pg_catalog."default",
    team_mascot character varying(50) COLLATE pg_catalog."default",
    team_abbrev_rs character varying(5) COLLATE pg_catalog."default" NOT NULL,
    team_abbrev_br character varying(5) COLLATE pg_catalog."default" NOT NULL,
    league character varying(2) COLLATE pg_catalog."default",
    first_season integer,
    last_season integer,
    regional_division character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT team_pkey PRIMARY KEY (team_key)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.team
    OWNER to babypng;