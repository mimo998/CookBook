TIERS = [(9.9, 'SS'), (9.0, 'S'), (8.5, 'A'), (7.5, 'B'), (6.0, 'C'), (5.0, 'D'), (3.0, 'E'), (0.0, 'F')]

class Ranking_List:

    def __init__(self):
        self.food = {}
        self.tiers = {}


    def ranking_sort(self):
        print("---Food Ranking---\n")
        sorted_food = dict(sorted(self.food.items(), key = lambda item : item[1], reverse= True))
        return sorted_food

    def print_ranking(self):
        ranking_list = self.ranking_sort()
        for name,rank in ranking_list.items():
            print(f"{float(rank):>4.1f} {name} \n")

        
    def insert_new_item(self,name, rank):
        if rank < 0 or rank > 10:
            raise ValueError("Rank must be between 0 and 10.")
        if name in self.food:
            raise ValueError(f"{name} already exists in the list.")
        self.food[name] = rank

    def change_item_rank(self,name, rank):
        if rank < 0 or rank > 10:
            raise ValueError("Rank must be between 0 and 10.")
        if name not in self.food:
            raise ValueError(f"{name} does not exist in the list.")
        self.food[name] = rank

    def remove_item(self,name):
        if name in self.food:
            del self.food[name]

    def tier_list(self):
        self.tiers = {tier: [] for _, tier in TIERS}
        for name, rank in self.food.items():
            for threshold, tier in TIERS:
                if rank >= threshold:
                    self.tiers[tier].append(name)
                    break





