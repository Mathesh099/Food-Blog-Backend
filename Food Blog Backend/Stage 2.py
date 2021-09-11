import sqlite3
conn = sqlite3.connect("food_blog.db")
cursor_name = conn.cursor()
cursor_name.execute("CREATE TABLE meals(meal_id INTEGER primary key, meal_name TEXT not null unique)")
cursor_name.execute("CREATE TABLE ingredients(ingredient_id INTEGER PRIMARY KEY, ingredient_name TEXT NOT NULL UNIQUE)")
cursor_name.execute("CREATE TABLE measures(measure_id INTEGER PRIMARY KEY, measure_name TEXT UNIQUE)")
cursor_name.execute("CREATE TABLE recipes(recipe_id INTEGER PRIMARY KEY, recipe_name TEXT NOT NULL, recipe_description TEXT)")
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

n_r = 0
while True:
    print("Pass the empty recipe name to exit.")
    name = input("Recipe name: ")
    if name != "":
        n_r += 1
        desc = input("Recipe description: ")
        cursor_name.execute("insert into recipes values (?,?,?)", (n_r, name, desc))
        conn.commit()
    else:
        break
conn.close()
