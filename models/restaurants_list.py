class Restaurants_List:

    def __init__(self, storage):
        self.storage = storage

    def add_restaurant(self, restaurant, rank):
        if rank < 0 or rank > 5:
            raise ValueError("Rank must be between 0 and 5.")
        if self.storage.get(restaurant) is not None:
            raise ValueError(f"{restaurant} already exists in the list.")
        self.storage.insert(restaurant, rank)

    def remove_restaurant(self, restaurant):
        if self.storage.get(restaurant) is None:
            raise ValueError(f"{restaurant} not found in the list.")
        self.storage.delete(restaurant)

    def change_restaurant_rank(self, restaurant, rank):
        if rank < 0 or rank > 5:
            raise ValueError("Rank must be between 0 and 5.")
        if self.storage.get(restaurant) is None:
            raise ValueError(f"{restaurant} not found in the list.")
        self.storage.update_rank(restaurant, rank)

    def get_restaurants(self):
        return self.storage.get_all()

    def ranking_sort(self):
        return dict(sorted(self.storage.get_all().items(), key=lambda item: item[1], reverse=True))
