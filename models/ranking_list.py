TIERS = [(9.9, 'SS'), (9.0, 'S'), (8.5, 'A'), (7.5, 'B'), (6.0, 'C'), (5.0, 'D'), (3.0, 'E'), (0.0, 'F')]

class Ranking_List:

    def __init__(self, storage):
        self.storage = storage
        self.tiers = {}

    def ranking_sort(self):
        print("---Food Ranking---\n")
        sorted_food = dict(sorted(self.storage.get_all().items(), key=lambda item: item[1], reverse=True))
        return sorted_food

    def print_ranking(self):
        ranking_list = self.ranking_sort()
        for name, rank in ranking_list.items():
            print(f"{float(rank):>4.1f} {name} \n")

    def insert_new_item(self, name, rank):
        if rank < 0 or rank > 10:
            raise ValueError("Rank must be between 0 and 10.")
        if self.storage.get(name) is not None:
            raise ValueError(f"{name} already exists in the list.")
        self.storage.insert(name, rank)

    def change_item_rank(self, name, rank):
        if rank < 0 or rank > 10:
            raise ValueError("Rank must be between 0 and 10.")
        if self.storage.get(name) is None:
            raise ValueError(f"{name} does not exist in the list.")
        self.storage.update_rank(name, rank)

    def remove_item(self, name):
        if self.storage.get(name) is None:
            raise ValueError(f"{name} not found in the list.")
        self.storage.delete(name)

    def tier_list(self):
        self.tiers = {tier: [] for _, tier in TIERS}
        for name, rank in self.storage.get_all().items():
            for threshold, tier in TIERS:
                if rank >= threshold:
                    self.tiers[tier].append(name)
                    break
