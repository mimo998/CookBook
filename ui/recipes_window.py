import tkinter as tk
from models.recipe import Recipe


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

        self.listbox = tk.Listbox(self.window, width=40)
        self.listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for name in sorted(self.recipe_list.recipes.keys()):
            self.listbox.insert(tk.END, name)

    def delete_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        name = self.listbox.get(selection[0])
        self.recipe_list.remove_recipe(name)
        self.refresh_list()

    def open_add_popup(self):
        popup = tk.Toplevel(self.window)
        popup.title("Add Recipe")

        tk.Label(popup, text="Name:").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1)

        tk.Label(popup, text="Ingredients (comma-separated):").grid(row=1, column=0, sticky="e")
        ingredients_entry = tk.Entry(popup)
        ingredients_entry.grid(row=1, column=1)

        tk.Label(popup, text="Time:").grid(row=2, column=0, sticky="e")
        time_entry = tk.Entry(popup)
        time_entry.grid(row=2, column=1)

        tk.Label(popup, text="Instructions:").grid(row=3, column=0, sticky="e")
        instructions_entry = tk.Entry(popup)
        instructions_entry.grid(row=3, column=1)

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(row=4, column=0, columnspan=2)

        def submit():
            try:
                name = name_entry.get()
                if not name:
                    raise ValueError("Name is required.")
                ingredients = [i.strip() for i in ingredients_entry.get().split(",") if i.strip()]
                time = time_entry.get()
                instructions = instructions_entry.get()

                recipe = Recipe(name, ingredients, time, instructions)
                self.recipe_list.add_recipe(recipe)
                self.refresh_list()
                popup.destroy()
            except ValueError as e:
                error_label.config(text=str(e))

        submit_button = tk.Button(popup, text="Submit", command=submit)
        submit_button.grid(row=5, column=0, columnspan=2)
