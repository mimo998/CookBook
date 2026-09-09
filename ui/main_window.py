import tkinter as tk
from ui.ranking_window import RankingWindow
from ui.restaurants_window import RestaurantsWindow
from ui.recipes_window import RecipesWindow
from ui.try_later_window import TryLaterWindow


class MainWindow:
    def __init__(self, root, ranking_list, restaurants_list, recipe_list, try_later_list):
        self.root = root
        self.root.title("CookBook")

        self.ranking_list = ranking_list
        self.restaurants_list = restaurants_list
        self.recipe_list = recipe_list
        self.try_later_list = try_later_list

        self.food_ranking_button = tk.Button(
            root, text="Food Ranking", command=self.open_ranking_window
        )
        self.food_ranking_button.pack(side="left")

        self.restaurants_button = tk.Button(
            root, text="Restaurants", command=self.open_restaurants_window
        )
        self.restaurants_button.pack(side="left")

        self.recipes_button = tk.Button(
            root, text="Recipes", command=self.open_recipes_window
        )
        self.recipes_button.pack(side="left")

        self.try_later_button = tk.Button(
            root, text="Try Later", command=self.open_try_later_window
        )
        self.try_later_button.pack(side="left")

    def open_ranking_window(self):
        RankingWindow(self.root, self.ranking_list)

    def open_restaurants_window(self):
        RestaurantsWindow(self.root, self.restaurants_list)

    def open_recipes_window(self):
        RecipesWindow(self.root, self.recipe_list)

    def open_try_later_window(self):
        TryLaterWindow(self.root, self.try_later_list, self.ranking_list)
