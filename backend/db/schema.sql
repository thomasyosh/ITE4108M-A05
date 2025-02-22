
CREATE TABLE IF NOT EXISTS public.recipes
(
    id integer NOT NULL,
    title character varying(255) COLLATE pg_catalog."default",
    date date,
    description text COLLATE pg_catalog."default",
    cooking_time character varying(100) COLLATE pg_catalog."default",
    serving_size character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT recipes_pkey PRIMARY KEY (id)
)





CREATE TABLE IF NOT EXISTS public.ingredients
(
    id integer NOT NULL,
    recipe_id integer,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    quantity character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT ingredients_pkey PRIMARY KEY (id),
    CONSTRAINT ingredients_recipe_id_fkey FOREIGN KEY (recipe_id)
        REFERENCES public.recipes (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)


CREATE TABLE IF NOT EXISTS public.steps
(
    id integer NOT NULL,
    recipe_id integer,
    step_number integer NOT NULL,
    instruction text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT steps_pkey PRIMARY KEY (id),
    CONSTRAINT steps_recipe_id_fkey FOREIGN KEY (recipe_id)
        REFERENCES public.recipes (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
