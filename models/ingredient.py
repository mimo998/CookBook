class Ingredient:
    def __init__(self, name, amount, calories=None, unit=None, description=None):
        self.name = name
        self.amount = amount
        self.calories = calories
        self.unit = unit
        self.description = description

    def edit_ingredient(self, name=None, amount=None, calories=None, unit=None, description=None):
        if name is not None:
            self.name = name
        if amount is not None:
            self.amount = amount
        if calories is not None:
            self.calories = calories
        if unit is not None:
            self.unit = unit
        if description is not None:
            self.description = description
