from models.ingredient import Ingredient
from models.recipe import Recipe


class RecipeStorage:

    def __init__(self, connection):
        self.connection = connection

    def insert(self, name, ingredients, time, instructions):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO recipes (name, time, instructions) VALUES (?, ?, ?)",
            (name, time, instructions)
        )
        self._insert_ingredients(cursor, name, ingredients)
        self.connection.commit()

    def _insert_ingredients(self, cursor, recipe_name, ingredients):
        for ingredient in ingredients:
            cursor.execute(
                "INSERT INTO ingredients (recipe_name, name, amount, calories, unit, description) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (recipe_name, ingredient.name, ingredient.amount, ingredient.calories,
                 ingredient.unit, ingredient.description)
            )

    def get(self, name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, time, instructions FROM recipes WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row is None:
            return None
        name, time, instructions = row
        return Recipe(name, self._get_ingredients(cursor, name), time, instructions)

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, time, instructions FROM recipes")
        recipes = cursor.fetchall()

        result = {}
        for name, time, instructions in recipes:
            result[name] = Recipe(name, self._get_ingredients(cursor, name), time, instructions)
        return result

    def _get_ingredients(self, cursor, recipe_name):
        cursor.execute(
            "SELECT name, amount, calories, unit, description FROM ingredients WHERE recipe_name = ?",
            (recipe_name,)
        )
        rows = cursor.fetchall()
        return [
            Ingredient(name, amount, calories, unit, description)
            for name, amount, calories, unit, description in rows
        ]

    def update_recipe(self, name, new_name=None, new_ingredients=None, new_time=None, new_instructions=None):
        cursor = self.connection.cursor()
        if new_name:
            cursor.execute("UPDATE recipes SET name = ? WHERE name = ?", (new_name, name))
            cursor.execute("UPDATE ingredients SET recipe_name = ? WHERE recipe_name = ?", (new_name, name))
            name = new_name  # Update the name for subsequent updates
        if new_time:
            cursor.execute("UPDATE recipes SET time = ? WHERE name = ?", (new_time, name))
        if new_instructions:
            cursor.execute("UPDATE recipes SET instructions = ? WHERE name = ?", (new_instructions, name))
        if new_ingredients is not None:
            cursor.execute("DELETE FROM ingredients WHERE recipe_name = ?", (name,))
            self._insert_ingredients(cursor, name, new_ingredients)
        self.connection.commit()

    def delete(self, name):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM ingredients WHERE recipe_name = ?", (name,))
        cursor.execute("DELETE FROM recipes WHERE name = ?", (name,))
        self.connection.commit()
