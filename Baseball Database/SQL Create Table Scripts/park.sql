-- Table: public.park

-- DROP TABLE public.park;

CREATE TABLE public.park
(
    park_key integer NOT NULL,
    park_name character varying(100) COLLATE pg_catalog."default",
    team_key integer NOT NULL,
    park_open_date date NOT NULL,
    park_close_date date,
    park_zip_code character varying(6) COLLATE pg_catalog."default",
    turf_type character varying(20) COLLATE pg_catalog."default",
    roof_type character varying(30) COLLATE pg_catalog."default",
    seating_capacity integer,
    CONSTRAINT park_pkey PRIMARY KEY (park_key)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.park
    OWNER to babypng;