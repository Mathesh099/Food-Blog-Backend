import sqlite3
conn = sqlite3.connect("food_blog.db")
cursor_name = conn.cursor()
cursor_name.execute("CREATE TABLE meals(meal_id INTEGER primary key, meal_name TEXT not null unique)")
cursor_name.execute("CREATE TABLE ingredients(ingredient_id INTEGER PRIMARY KEY, ingredient_name TEXT NOT NULL UNIQUE)")
cursor_name.execute("CREATE TABLE measures(measure_id INTEGER PRIMARY KEY, measure_name TEXT UNIQUE)")
cursor_name.execute("CREATE TABLE recipes(recipe_id INTEGER PRIMARY KEY, recipe_name TEXT NOT NULL, recipe_description TEXT)")
cursor_name.execute("PRAGMA foreign_keys = ON;")
cursor_name.execute("CREATE TABLE serve (serve_id INT PRIMARY KEY, recipe_id INT NOT NULL, meal_id INT NOT NULL,"
                    "FOREIGN KEY(recipe_id) REFERENCES recipes (recipe_id), FOREIGN KEY(meal_id) REFERENCES "
                    "meals (meal_id));")
cursor_name.execute("CREATE TABLE quantity (quantity_id INT PRIMARY KEY, recipe_id INT NOT NULL, measure_id INT NOT NULL,ingredient_id INT NOT NULL,quantity INT NOT NULL,"
                    "FOREIGN KEY(recipe_id) REFERENCES recipes (recipe_id), FOREIGN KEY(measure_id) REFERENCES "
                    "measures (measure_id),FOREIGN KEY(ingredient_id) REFERENCES ingredients (ingredient_id));")
conn.commit()

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

for k, v in data.items():
        n = 0
        for n, item in enumerate(v):
            n += 1
            cursor_name.execute(f"insert into {k} values (?,?)", (n, item))
            conn.commit()

print("Pass the empty recipe name to exit.")
name = input("Recipe name: ")
n_r = 1
n_s = 0
while name:
    desc = input("Recipe description: ")
    cursor_name.execute("insert into recipes values (?,?,?)", (n_r, name, desc))
    conn.commit()
    n_m = input("1) breakfast  2) brunch  3) lunch  4) supper \nWhen the dish can be served:").split()
    for i in n_m:
        n_s += 1
        cursor_name.execute(f"INSERT INTO serve (serve_id, recipe_id, meal_id) VALUES (?, ?, ?);",
                            (n_s, n_r, i))
    ingredient_quantity = input("Input quantity of ingredient <press enter to stop>: ").split()
    reci_id = 0
    while ingredient_quantity:
        quantity, measure, ingredient = ingredient_quantity[0], ingredient_quantity[1], ingredient_quantity[-1]
        if "berry" in ingredient:
            measure = ""
        if measure not in data["measures"]:
            print("The measure is not conclusive!")
            ingredient_quantity = input("Input quantity of ingredient <press enter to stop>: ").split()
            continue
        ingredient_contains = [(1, n+1) for n, ing in enumerate(data["ingredients"]) if ingredient in ing]
        if sum([pair[0] for pair in ingredient_contains]) != 1:
            print("The measure is not conclusive!")
            ingredient_quantity = input("Input quantity of ingredient <press enter to stop>: ").split()
            continue
        cursor_name.execute(f"INSERT INTO quantity (quantity, recipe_id, measure_id, ingredient_id) VALUES (?, ?, ?, ?);",
                            (quantity, n_r, data["measures"].index(measure) + 1, ingredient_contains[0][1]))
        ingredient_quantity = input("Input quantity of ingredient <press enter to stop>: ").split()
    n_r += 1
    name = input("Recipe name: ")

conn.commit()
conn.close()
