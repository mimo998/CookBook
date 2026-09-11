import tkinter as tk
from models.recipe import Recipe
from models.ingredient import Ingredient
from services.recipe_importer import import_recipe_from_url


class RecipesFrame(tk.Frame):
    def __init__(self, parent, recipe_list, show_home, mainwindow):
        super().__init__(parent)
        self.recipe_list = recipe_list
        self.mainwindow = mainwindow

        header = tk.Frame(self)
        header.pack(fill="x", padx=10, pady=(10, 4))
        tk.Button(header, text="\u2190 Back", command=show_home).pack(side="left")
        tk.Label(header, text="Recipes", font=("Segoe UI", 14, "bold")).pack(side="left", padx=12)

        body = tk.Frame(self)
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        button_frame = tk.Frame(body)
        button_frame.pack(side="left", fill="y", padx=(0, 8))

        for text, command in [
            ("Add", self.open_add_popup),
            ("Edit", self.open_edit_popup),
            ("Delete", self.delete_selected),
            ("Import from URL", self.open_import_popup),
        ]:
            tk.Button(button_frame, text=text, width=14, command=command).pack(fill="x", pady=2)

        self.listbox = tk.Listbox(body, font=("Consolas", 11))
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(body, command=self.listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind("<Double-Button-1>", self.open_recipe_view)

        self.refresh_list()

    def open_recipe_view(self, event):
        name = self._selected_name()
        if name is None:
            return
        recipe = self.recipe_list.get_recipe(name)
        if recipe is None:
            return
        self.mainwindow.show_recipe_detail(recipe)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for name in sorted(self.recipe_list.get_all_recipes().keys()):
            self.listbox.insert(tk.END, name)

    def _selected_name(self):
        selection = self.listbox.curselection()
        if not selection:
            return None
        return self.listbox.get(selection[0])

    def delete_selected(self):
        name = self._selected_name()
        if name is None:
            return
        self.recipe_list.remove_recipe(name)
        self.refresh_list()

    def _new_popup(self, title):
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        return popup

    # ---- shared ingredients sub-editor, used by both Add and Edit popups ----

    def _build_ingredients_section(self, popup, row, initial_ingredients=None):
        """Adds an ingredients list + Add/Remove controls to `popup` at `row`.
        Returns the live list of Ingredient objects being built up."""
        ingredients = list(initial_ingredients) if initial_ingredients else []

        tk.Label(popup, text="Ingredients:").grid(row=row, column=0, sticky="ne", padx=6, pady=6)

        ingredients_listbox = tk.Listbox(popup, width=34, height=6)
        ingredients_listbox.grid(row=row, column=1, sticky="w", padx=6, pady=6)

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
            ingredient_popup.transient(popup)
            ingredient_popup.grab_set()

            fields = {}
            for i, (label, key) in enumerate([
                ("Name:", "name"),
                ("Amount:", "amount"),
                ("Unit:", "unit"),
                ("Calories (optional):", "calories"),
                ("Description (optional):", "description"),
            ]):
                tk.Label(ingredient_popup, text=label).grid(row=i, column=0, sticky="e", padx=6, pady=4)
                entry = tk.Entry(ingredient_popup)
                entry.grid(row=i, column=1, padx=6, pady=4)
                fields[key] = entry

            ingredient_error_label = tk.Label(ingredient_popup, text="", fg="red")
            ingredient_error_label.grid(row=5, column=0, columnspan=2)

            def submit_ingredient():
                name = fields["name"].get()
                amount = fields["amount"].get()
                unit = fields["unit"].get()
                calories_text = fields["calories"].get()
                description = fields["description"].get()

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

            tk.Button(ingredient_popup, text="Add", command=submit_ingredient).grid(
                row=6, column=0, columnspan=2, pady=(0, 8))

        controls_frame = tk.Frame(popup)
        controls_frame.grid(row=row, column=2, sticky="n", pady=6)
        tk.Button(controls_frame, text="Add Ingredient", width=14,
                  command=open_add_ingredient_popup).pack(fill="x", pady=2)
        tk.Button(controls_frame, text="Remove Selected", width=14,
                  command=remove_selected_ingredient).pack(fill="x", pady=2)

        refresh_ingredients_listbox()
        return ingredients

    # ---- Edit Recipe ----

    def open_edit_popup(self):
        name = self._selected_name()
        if name is None:
            return
        recipe = self.recipe_list.get_recipe(name)

        popup = self._new_popup("Edit Recipe")

        tk.Label(popup, text="Name:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        name_entry = tk.Entry(popup, width=34)
        name_entry.insert(0, recipe.name)
        name_entry.grid(row=0, column=1, padx=6, pady=6)

        tk.Label(popup, text="Time:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        time_entry = tk.Entry(popup, width=34)
        time_entry.insert(0, recipe.time)
        time_entry.grid(row=1, column=1, padx=6, pady=6)

        tk.Label(popup, text="Instructions:").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        instructions_entry = tk.Entry(popup, width=34)
        instructions_entry.insert(0, recipe.instructions)
        instructions_entry.grid(row=2, column=1, padx=6, pady=6)

        ingredients = self._build_ingredients_section(popup, row=3, initial_ingredients=recipe.ingredients)

        self.error_label = tk.Label(popup, text="", fg="red")
        self.error_label.grid(row=4, column=0, columnspan=3)

        tk.Button(
            popup, text="Submit",
            command=lambda: self.submit_edit(
                recipe, name_entry.get(), ingredients, time_entry.get(), instructions_entry.get(), popup
            )
        ).grid(row=5, column=0, columnspan=3, pady=(0, 8))

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
        popup = self._new_popup("Import Recipe from URL")

        tk.Label(popup, text="Recipe URL:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        url_entry = tk.Entry(popup, width=46)
        url_entry.grid(row=0, column=1, padx=6, pady=6)

        error_label = tk.Label(popup, text="", fg="red", wraplength=380, justify="left")
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

        tk.Button(popup, text="Import", command=submit).grid(row=2, column=0, columnspan=2, pady=(0, 8))

    # ---- Add Recipe ----

    def open_add_popup(self):
        popup = self._new_popup("Add Recipe")

        tk.Label(popup, text="Name:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        name_entry = tk.Entry(popup, width=34)
        name_entry.grid(row=0, column=1, padx=6, pady=6)

        tk.Label(popup, text="Time:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        time_entry = tk.Entry(popup, width=34)
        time_entry.grid(row=1, column=1, padx=6, pady=6)

        tk.Label(popup, text="Instructions:").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        instructions_entry = tk.Entry(popup, width=34)
        instructions_entry.grid(row=2, column=1, padx=6, pady=6)

        ingredients = self._build_ingredients_section(popup, row=3)

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(row=4, column=0, columnspan=3)

        def submit():
            try:
                name = name_entry.get()
                if not name:
                    raise ValueError("Name is required.")
                if not ingredients:
                    raise ValueError("Add at least one ingredient.")
                recipe = Recipe(name, list(ingredients), time_entry.get(), instructions_entry.get())
                self.recipe_list.add_recipe(recipe)
                self.refresh_list()
                popup.destroy()
            except ValueError as e:
                error_label.config(text=str(e))

        tk.Button(popup, text="Submit", command=submit).grid(row=5, column=0, columnspan=3, pady=(0, 8))
