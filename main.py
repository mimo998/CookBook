import tkinter as tk
from database.db_setup import get_connection, setup_database
from database.ranking_storage import RankingStorage
from database.restaurant_storage import RestaurantStorage
from database.recipe_storage import RecipeStorage
from database.try_later_storage import TryLaterStorage
from models.ranking_list import Ranking_List
from models.restaurants_list import Restaurants_List
from models.recipe_list import Recipe_List
from models.try_later_list import Try_Later_List
from ui.main_window import MainWindow

connection = get_connection()
setup_database(connection)

ranking_list = Ranking_List(RankingStorage(connection))
restaurants_list = Restaurants_List(RestaurantStorage(connection))
recipe_list = Recipe_List(RecipeStorage(connection))
try_later_list = Try_Later_List(TryLaterStorage(connection))

root = tk.Tk()
app = MainWindow(root, ranking_list, restaurants_list, recipe_list, try_later_list)
root.mainloop()
