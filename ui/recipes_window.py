import tkinter as tk
from models.recipe import Recipe
from models.ingredient import Ingredient
from services.recipe_importer import import_recipe_from_url


class RecipesWindow:
    def __init__(self, root, recipe_list):
        self.recipe_list = recipe_list

        self.window = tk.Toplevel(root)
        self.window.title("Recipes")

        button_frame = tk.Frame(self.window)
        button_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.add_button = tk.Button(button_frame, text="Add", command=self.open_add_popup)
        self.add_button.pack(fill="x")

        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_selected)
        self.delete_button.pack(fill="x")

        self.edit_button = tk.Button(button_frame, text="Edit", command=self.open_edit_popup)
        self.edit_button.pack(fill="x")

        self.import_button = tk.Button(button_frame, text="Import from URL", command=self.open_import_popup)
        self.import_button.pack(fill="x")

        self.listbox = tk.Listbox(self.window, width=40)
        self.listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for name in sorted(self.recipe_list.get_all_recipes().keys()):
            self.listbox.insert(tk.END, name)

    def delete_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        name = self.listbox.get(selection[0])
        self.recipe_list.remove_recipe(name)
        self.refresh_list()

    # ---- shared ingredients sub-editor, used by both Add and Edit popups ----

    def _build_ingredients_section(self, popup, row, initial_ingredients=None):
        """Adds an ingredients list + Add/Remove controls to `popup` at `row`.
        Returns the live list of Ingredient objects being built up."""
        ingredients = list(initial_ingredients) if initial_ingredients else []

        tk.Label(popup, text="Ingredients:").grid(row=row, column=0, sticky="ne")

        ingredients_listbox = tk.Listbox(popup, width=32, height=5)
        ingredients_listbox.grid(row=row, column=1, sticky="w")

        def refresh_ingredients_listbox():
            ingredients_listbox.delete(0, tk.END)
            for ingredient in ingredients:
                summary = f"{ingredient.name} - {ingredient.amount}"
                if ingredient.unit:
                    summary += f" {ingredient.unit}"
                if ingredient.calories is not None:
                    summary += f" ({ingredient.calories} cal)"
                ingredients_listbox.insert(tk.END, summary)

        def remove_selected_ingredient():
            selection = ingredients_listbox.curselection()
            if not selection:
                return
            del ingredients[selection[0]]
            refresh_ingredients_listbox()

        def open_add_ingredient_popup():
            ingredient_popup = tk.Toplevel(popup)
            ingredient_popup.title("Add Ingredient")

            tk.Label(ingredient_popup, text="Name:").grid(row=0, column=0, sticky="e")
            name_entry = tk.Entry(ingredient_popup)
            name_entry.grid(row=0, column=1)

            tk.Label(ingredient_popup, text="Amount:").grid(row=1, column=0, sticky="e")
            amount_entry = tk.Entry(ingredient_popup)
            amount_entry.grid(row=1, column=1)

            tk.Label(ingredient_popup, text="Unit:").grid(row=2, column=0, sticky="e")
            unit_entry = tk.Entry(ingredient_popup)
            unit_entry.grid(row=2, column=1)

            tk.Label(ingredient_popup, text="Calories (optional):").grid(row=3, column=0, sticky="e")
            calories_entry = tk.Entry(ingredient_popup)
            calories_entry.grid(row=3, column=1)

            tk.Label(ingredient_popup, text="Description (optional):").grid(row=4, column=0, sticky="e")
            description_entry = tk.Entry(ingredient_popup)
            description_entry.grid(row=4, column=1)

            ingredient_error_label = tk.Label(ingredient_popup, text="", fg="red")
            ingredient_error_label.grid(row=5, column=0, columnspan=2)

            def submit_ingredient():
                name = name_entry.get()
                amount = amount_entry.get()
                unit = unit_entry.get()
                calories_text = calories_entry.get()
                description = description_entry.get()

                if not name or not amount:
                    ingredient_error_label.config(text="Name and amount are required.")
                    return

                try:
                    calories = float(calories_text) if calories_text else None
                except ValueError:
                    ingredient_error_label.config(text="Calories must be a number.")
                    return

                ingredients.append(Ingredient(name, amount, calories, unit or None, description or None))
                refresh_ingredients_listbox()
                ingredient_popup.destroy()

            submit_button = tk.Button(ingredient_popup, text="Add", command=submit_ingredient)
            submit_button.grid(row=6, column=0, columnspan=2)

        controls_frame = tk.Frame(popup)
        controls_frame.grid(row=row, column=2, sticky="n")
        tk.Button(controls_frame, text="Add Ingredient", command=open_add_ingredient_popup).pack(fill="x")
        tk.Button(controls_frame, text="Remove Selected", command=remove_selected_ingredient).pack(fill="x")

        refresh_ingredients_listbox()
        return ingredients

    # ---- Edit Recipe ----

    def open_edit_popup(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        name = self.listbox.get(selection[0])
        recipe = self.recipe_list.get_recipe(name)

        popup = tk.Toplevel(self.window)
        popup.title("Edit Recipe")

        tk.Label(popup, text="Name:").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(popup)
        name_entry.insert(0, recipe.name)
        name_entry.grid(row=0, column=1)

        tk.Label(popup, text="Time:").grid(row=1, column=0, sticky="e")
        time_entry = tk.Entry(popup)
        time_entry.insert(0, recipe.time)
        time_entry.grid(row=1, column=1)

        tk.Label(popup, text="Instructions:").grid(row=2, column=0, sticky="e")
        instructions_entry = tk.Entry(popup)
        instructions_entry.insert(0, recipe.instructions)
        instructions_entry.grid(row=2, column=1)

        ingredients = self._build_ingredients_section(popup, row=3, initial_ingredients=recipe.ingredients)

        self.error_label = tk.Label(popup, text="", fg="red")
        self.error_label.grid(row=4, column=0, columnspan=2)

        submit_button = tk.Button(
            popup, text="Submit",
            command=lambda: self.submit_edit(
                recipe, name_entry.get(), ingredients, time_entry.get(), instructions_entry.get(), popup
            )
        )
        submit_button.grid(row=5, column=0, columnspan=2)

    def submit_edit(self, recipe, new_name, new_ingredients, new_time, new_instructions, popup):
        try:
            if not new_name:
                raise ValueError("Name is required.")
            if not new_ingredients:
                raise ValueError("Add at least one ingredient.")
            self.recipe_list.edit_recipe(
                recipe.name, new_name=new_name, new_ingredients=list(new_ingredients),
                new_time=new_time, new_instructions=new_instructions
            )
            self.refresh_list()
            popup.destroy()
        except ValueError as e:
            self.error_label.config(text=str(e))

    # ---- Import Recipe from URL ----

    def open_import_popup(self):
        popup = tk.Toplevel(self.window)
        popup.title("Import Recipe from URL")

        tk.Label(popup, text="Recipe URL:").grid(row=0, column=0, sticky="e")
        url_entry = tk.Entry(popup, width=40)
        url_entry.grid(row=0, column=1)

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(row=1, column=0, columnspan=2)

        def submit():
            try:
                url = url_entry.get()
                if not url:
                    raise ValueError("Enter a URL.")
                recipe = import_recipe_from_url(url)
                self.recipe_list.add_recipe(recipe)
                self.refresh_list()
                popup.destroy()
            except ValueError as e:
                error_label.config(text=str(e))

        submit_button = tk.Button(popup, text="Import", command=submit)
        submit_button.grid(row=2, column=0, columnspan=2)

    # ---- Add Recipe ----

    def open_add_popup(self):
        popup = tk.Toplevel(self.window)
        popup.title("Add Recipe")

        tk.Label(popup, text="Name:").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1)

        tk.Label(popup, text="Time:").grid(row=1, column=0, sticky="e")
        time_entry = tk.Entry(popup)
        time_entry.grid(row=1, column=1)

        tk.Label(popup, text="Instructions:").grid(row=2, column=0, sticky="e")
        instructions_entry = tk.Entry(popup)
        instructions_entry.grid(row=2, column=1)

        ingredients = self._build_ingredients_section(popup, row=3)

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(row=4, column=0, columnspan=2)

        def submit():
            try:
                name = name_entry.get()
                if not name:
                    raise ValueError("Name is required.")
                if not ingredients:
                    raise ValueError("Add at least one ingredient.")
                time = time_entry.get()
                instructions = instructions_entry.get()

                recipe = Recipe(name, list(ingredients), time, instructions)
                self.recipe_list.add_recipe(recipe)
                self.refresh_list()
                popup.destroy()
            except ValueError as e:
                error_label.config(text=str(e))

        submit_button = tk.Button(popup, text="Submit", command=submit)
        submit_button.grid(row=5, column=0, columnspan=2)
