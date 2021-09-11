import sqlite3
import argparse

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}
parser = argparse.ArgumentParser()
parser.add_argument("db")
parser.add_argument("--ingredients")
parser.add_argument("--meals")
args = parser.parse_args()
conn = sqlite3.connect(args.db)
cursor_name = conn.cursor()
if args.ingredients is None and args.meals is None:
    cursor_name.execute("CREATE TABLE IF NOT EXISTS meals(meal_id INTEGER primary key, meal_name TEXT not null unique)")
    cursor_name.execute("CREATE TABLE IF NOT EXISTS ingredients(ingredient_id INTEGER primary key, ingredient_name TEXT not null unique)")
    cursor_name.execute("CREATE TABLE IF NOT EXISTS measures(measure_id INTEGER primary key, measure_name TEXT unique)")
    cursor_name.execute("CREATE TABLE IF NOT EXISTS recipes(recipe_id INTEGER primary key, recipe_name TEXT not null, recipe_description TEXT)")
    cursor_name.execute("PRAGMA foreign_keys = ON;")
    cursor_name.execute("CREATE TABLE IF NOT EXISTS serve (serve_id INT PRIMARY KEY, recipe_id INT NOT NULL, meal_id INT NOT NULL,"
                        "FOREIGN KEY(recipe_id) REFERENCES recipes (recipe_id), FOREIGN KEY(meal_id) REFERENCES "
                        "meals (meal_id));")
    cursor_name.execute("CREATE TABLE IF NOT EXISTS quantity (quantity_id INT PRIMARY KEY, recipe_id INT NOT NULL, measure_id INT NOT NULL,ingredient_id INT NOT NULL,quantity INT NOT NULL,"
                        "FOREIGN KEY(recipe_id) REFERENCES recipes (recipe_id), FOREIGN KEY(measure_id) REFERENCES "
                        "measures (measure_id),FOREIGN KEY(ingredient_id) REFERENCES ingredients (ingredient_id));")

    conn.commit()
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
else:
    ing = args.ingredients.split(",")
    meal = args.meals.split(",")
    try:
        ing = list(map(lambda x: data["ingredients"].index(x) + 1, ing))
        meal = tuple(map(lambda x: data["meals"].index(x) + 1, meal))
    except ValueError:
        print("There are no such recipes in the database")
        exit()
    all_recipe = []
    for m in meal:
        all_recipe.extend(cursor_name.execute(f"select recipe_id from serve where meal_id=?", (m,)).fetchall())
    all_recipe = list(map(lambda x: x[0], all_recipe))
    all_ing = []
    for r in all_recipe:
        all_ing.extend(cursor_name.execute(f"select recipe_id,ingredient_id from quantity where recipe_id=?", (r,)).fetchall())
    final = {}
    for r, i in all_ing:
        if r in final:
            final[r].append(i)
        else:
            final[r] = [i]
    final_recipe_id = []
    for k, v in final.items():
        if all(item in v for item in ing):
            final_recipe_id.extend(cursor_name.execute(f"select recipe_name from recipes where recipe_id=?", (k,)).fetchall())
    if final_recipe_id:
        print(*final_recipe_id)
    else:
        print("There are no such recipes in the database")
conn.close()
