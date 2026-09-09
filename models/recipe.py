class Recipe:

    def __init__(self,name,ingredients, time, instructions):
        self.name = name
        self.ingredients = ingredients
        self.time = time
        self.instructions = instructions
        self.image = None # TODO

    def print_recipe(self):
        pass

    def edit_recipe(self, name=None, ingredients=None, time=None, instructions=None):
        if name is not None:
            self.name = name
        if ingredients is not None:
            self.ingredients = ingredients
        if time is not None:
            self.time = time
        if instructions is not None:
            self.instructions = instructions

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def remove_ingredient(self, name):
        self.ingredients = [ingredient for ingredient in self.ingredients if ingredient.name != name]
