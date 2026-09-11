import tkinter as tk
from ui.ranking_window import RankingFrame
from ui.restaurants_window import RestaurantsFrame
from ui.recipes_window import RecipesFrame
from ui.try_later_window import TryLaterFrame
from ui.recipe_detail import RecipeDetailFrame


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


class MainWindow:
    def __init__(self, root, ranking_list, restaurants_list, recipe_list, try_later_list):
        self.root = root
        self.root.title("CookBook")
        center_window(self.root, 720, 480)
        self.root.minsize(560, 380)

        self.ranking_list = ranking_list
        self.restaurants_list = restaurants_list
        self.recipe_list = recipe_list
        self.try_later_list = try_later_list

        # Everything lives inside this one container; we swap what's in it.
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.current_frame = None
        self.show_home()

    def _swap_to(self, frame):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    def show_home(self):
        self._swap_to(HomeFrame(self.container, self))

    def show_ranking(self):
        self._swap_to(RankingFrame(self.container, self.ranking_list, self.show_home))

    def show_restaurants(self):
        self._swap_to(RestaurantsFrame(self.container, self.restaurants_list, self.show_home))

    def show_recipes(self):
        self._swap_to(RecipesFrame(self.container, self.recipe_list, self.show_home, self))

    def show_try_later(self):
        self._swap_to(TryLaterFrame(self.container, self.try_later_list, self.ranking_list, self.show_home))

    def show_recipe_detail(self, recipe):
        self._swap_to(RecipeDetailFrame(self.container, recipe, self.show_recipes))


class HomeFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        tk.Label(self, text="CookBook", font=("Segoe UI", 24, "bold")).pack(pady=(40, 6))
        tk.Label(self, text="Your personal food book", font=("Segoe UI", 10)).pack(pady=(0, 30))

        buttons = [
            ("Food Ranking", app.show_ranking),
            ("Restaurants", app.show_restaurants),
            ("Recipes", app.show_recipes),
            ("Try Later", app.show_try_later),
        ]
        for text, command in buttons:
            tk.Button(self, text=text, width=24, height=2, command=command).pack(pady=4)
