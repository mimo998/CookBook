import tkinter as tk
from models.ranking_list import Ranking_List
from models.restaurants_list import Restaurants_List
from models.recipe_list import Recipe_List
from ui.ranking_window import RankingWindow
from ui.restaurants_window import RestaurantsWindow
from ui.recipes_window import RecipesWindow


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("CookBook")

        self.ranking_list = Ranking_List()
        self.restaurants_list = Restaurants_List()
        self.recipe_list = Recipe_List()

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

    def open_ranking_window(self):
        RankingWindow(self.root, self.ranking_list)

    def open_restaurants_window(self):
        RestaurantsWindow(self.root, self.restaurants_list)

    def open_recipes_window(self):
        RecipesWindow(self.root, self.recipe_list)
