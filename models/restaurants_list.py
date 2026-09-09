class Restaurants_List:

    def __init__(self):
        self.restaurants = {}

    def add_restaurant(self, restaurant, rank):
        if rank < 0 or rank > 5:
            raise ValueError("Rank must be between 0 and 5.")
        self.restaurants[restaurant] = rank

    def remove_restaurant(self, restaurant):
        if restaurant in self.restaurants:
            del self.restaurants[restaurant]
        else:
            print(f"{restaurant} not found in the list.")

    def change_restaurant_rank(self, restaurant, rank):
        if rank < 0 or rank > 5:
            raise ValueError("Rank must be between 0 and 5.")
        if restaurant in self.restaurants:
            self.restaurants[restaurant] = rank
        else:
            print(f"{restaurant} not found in the list.")

    def get_restaurants(self):
        return self.restaurants

    def ranking_sort(self):
        sorted_restaurants = dict(sorted(self.restaurants.items(), key = lambda item : item[1], reverse= True))
        return sorted_restaurants


