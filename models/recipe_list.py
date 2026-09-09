from models.recipe import Recipe
class Recipe_List:

    def __init__(self,storage):
        self.storage = storage

    def get_recipe(self, name):
        recipe = self.storage.get(name)
        if recipe is None:
            raise ValueError(f"{name} does not exist in the list.")
        return recipe

    def get_all_recipes(self):
        return self.storage.get_all()
    
    def add_recipe(self, recipe):
        if not isinstance(recipe, Recipe):
            raise ValueError("The object must be an instance of the Recipe class.")
        if self.storage.get(recipe.name) is not None:
            raise ValueError(f"{recipe.name} already exists in the list.")
        self.storage.insert(recipe.name, recipe.ingredients, recipe.time, recipe.instructions)

    def edit_recipe(self, name, new_name=None, new_ingredients=None, new_time=None, new_instructions=None):
        if self.storage.get(name) is None:
            raise ValueError(f"{name} does not exist in the list.")
        if new_name is not None and new_name != name and self.storage.get(new_name) is not None:
            raise ValueError(f"{new_name} already exists in the list.")
        self.storage.update_recipe(name, new_name, new_ingredients, new_time, new_instructions)

    def remove_recipe(self, name):
        if self.storage.get(name) is None:
            raise ValueError(f"{name} does not exist in the list.")
        self.storage.delete(name)