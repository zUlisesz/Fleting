
CREATE TABLE recipes (
    id VARCHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- 2. Master list of ingredients
CREATE TABLE ingredients (
    id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL UNIQUE,
    unit VARCHAR(50) NULL,             
    PRIMARY KEY (id)
);


CREATE TABLE recipe_ingredients (
    id VARCHAR(36) NOT NULL,
    recipe_id VARCHAR(36) NOT NULL,
    ingredient_id VARCHAR(36) NOT NULL,
    amount VARCHAR(100) NULL,          
    PRIMARY KEY (id),
    CONSTRAINT fk_ri_recipe FOREIGN KEY (recipe_id)
        REFERENCES recipes(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_ri_ingredient FOREIGN KEY (ingredient_id)
        REFERENCES ingredients(id)
        ON DELETE CASCADE
);


CREATE TABLE recipe_instructions (
    id VARCHAR(36) NOT NULL,
    recipe_id VARCHAR(36) NOT NULL,
    step_number INT NOT NULL,           
    instruction TEXT NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_instructions_recipe FOREIGN KEY (recipe_id)
        REFERENCES recipes(id)
        ON DELETE CASCADE
);
