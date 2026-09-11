import tkinter as tk
from tkinter import ttk
from models.recipe import Recipe

class RecipeDetailFrame(tk.Frame):
    def __init__(self, parent, recipe: Recipe, go_back):
        super().__init__(parent)
        self.recipe = recipe
        self.go_back = go_back

        header = tk.Frame(self)
        header.pack(fill="x", padx=10, pady=(10, 4))
        tk.Button(header, text="\u2190 Back", command=self.go_back).pack(side="left")
        tk.Label(header, text=recipe.name, font=("Segoe UI", 14, "bold")).pack(side="left", padx=12)

        if recipe.time:
            tk.Label(self, text=f"Time: {recipe.time}", font=("Segoe UI", 10)).pack(anchor="w", padx=12)

        tk.Label(self, text="Ingredients", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(8, 2))

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        tree = ttk.Treeview(
            tree_frame,
            columns=("name", "amount", "unit", "calories", "description"),
            show="headings"
        )
        tree.heading("name", text="Ingredient")
        tree.heading("amount", text="Amount")
        tree.heading("unit", text="Unit")
        tree.heading("calories", text="Calories")
        tree.heading("description", text="Description")
        tree.column("name", width=220)
        tree.column("amount", width=70)
        tree.column("unit", width=70)
        tree.column("calories", width=70)
        tree.column("description", width=200)

        for ing in self.recipe.ingredients:
            tree.insert(
                "",
                "end",
                values=(ing.name, ing.amount, ing.unit or "", ing.calories or "", ing.description or "")
            )
        tree_scroll = tk.Scrollbar(tree_frame, command=tree.yview)
        tree.config(yscrollcommand=tree_scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        tk.Label(self, text="Instructions", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(4, 2))

        text_frame = tk.Frame(self)
        text_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        instructions = tk.Text(text_frame, wrap="word", height=8, font=("Segoe UI", 10))
        instructions.pack(side="left", fill="both", expand=True)

        text_scroll = tk.Scrollbar(text_frame, command=instructions.yview)
        text_scroll.pack(side="right", fill="y")
        instructions.config(yscrollcommand=text_scroll.set)

        instructions.insert("1.0", recipe.instructions or "")
        instructions.config(state="disabled")   # read-only — must come AFTER insert

