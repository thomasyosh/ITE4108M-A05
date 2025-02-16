
DROP TABLE recipes CASCADE;
DROP TABLE steps CASCADE;
DROP TABLE ingredients CASCADE;

CREATE TABLE recipes (
  id INT PRIMARY KEY,
  title VARCHAR(255),
  date DATE ,
  description TEXT,
  cooking_time VARCHAR(100) ,
  serving_size VARCHAR(100)
);

CREATE TABLE steps (
  id INT PRIMARY KEY,
  recipe_id INT REFERENCES recipes(id) ON DELETE CASCADE,
  step_number INT NOT NULL,
  instruction TEXT NOT NULL
);

CREATE TABLE ingredients (
  id INT PRIMARY KEY,
  recipe_id INT REFERENCES recipes(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  quantity VARCHAR(100) NOT NULL
);

CREATE INDEX idx_ingredients_recipe ON ingredients(recipe_id);
CREATE INDEX idx_steps_recipe ON steps(recipe_id);

