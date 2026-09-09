class Recipe:

    def __init__(self,name,ingredients, time, instructions):
        self.name = name
        self.ingredients = ingredients
        self.time = time
        self.instructions = instructions
        self.image = None # TODO

    def print_recipe(self):
        pass

    def edit_ingredients(self, ingredients):
        self.ingredients = ingredients

    def edit_instructions(self,instructions):
        self.instructions = instructions

    def remove_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            self.ingredients.remove(ingredient)
