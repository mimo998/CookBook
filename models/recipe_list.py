from models.recipe import Recipe
class Recipe_List:
    def __init__(self):
        self.recipes = {}

    def get_recipe(self, name):
        return self.recipes.get(name)

    def add_recipe(self,recipe):
        if not isinstance(recipe, Recipe):
            raise ValueError("The object must be an instance of the Recipe class.")
        self.recipes[recipe.name] = recipe

    def remove_recipe(self, name):
        if name in self.recipes:
            del self.recipes[name]
        else:
            print(f"{name} not found in the list.")