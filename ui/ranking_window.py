import tkinter as tk


class RankingWindow:
    def __init__(self, root, ranking_list):
        self.ranking_list = ranking_list

        self.window = tk.Toplevel(root)
        self.window.title("Food Ranking")

        # Left side: Add / Delete buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.add_button = tk.Button(button_frame, text="Add", command=self.open_add_popup)
        self.add_button.pack(fill="x")

        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_selected)
        self.delete_button.pack(fill="x")

        self.edit_button = tk.Button(button_frame, text="Edit", command=self.open_edit_popup)
        self.edit_button.pack(fill="x")

        self.tier_list = tk.Button(button_frame, text="Tier List", command=self.open_tier_list)
        self.tier_list.pack(fill="x")

        # Right side: the list itself
        self.listbox = tk.Listbox(self.window, width=40)
        self.listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for name, rank in self.ranking_list.ranking_sort().items():
            self.listbox.insert(tk.END, f"{rank:>4.1f}  {name}")

    def delete_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        selected_text = self.listbox.get(selection[0])
        name = selected_text.split(maxsplit=1)[1]  # strip the "rank  " prefix
        self.ranking_list.remove_item(name)
        self.refresh_list()

    def open_edit_popup(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        selected_text = self.listbox.get(selection[0])
        name = selected_text.split(maxsplit=1)[1]  # strip the "rank  " prefix

        popup = tk.Toplevel(self.window)
        popup.title("Edit Food Ranking")

        tk.Label(popup, text="New Rank (0-10):").grid(row=0, column=0, sticky="e")
        rank_entry = tk.Entry(popup)
        rank_entry.grid(row=0, column=1)

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(row=1, column=0, columnspan=2)

        def submit():
            try:
                rank = float(rank_entry.get())
                self.ranking_list.change_item_rank(name, rank)
                self.refresh_list()
                popup.destroy()
            except ValueError as e:
                error_label.config(text=str(e))

        submit_button = tk.Button(popup, text="Submit", command=submit)
        submit_button.grid(row=2, column=0, columnspan=2)

    def open_add_popup(self):
        popup = tk.Toplevel(self.window)
        popup.title("Add Food Ranking")

        tk.Label(popup, text="Name:").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1)

        tk.Label(popup, text="Rank (0-10):").grid(row=1, column=0, sticky="e")
        rank_entry = tk.Entry(popup)
        rank_entry.grid(row=1, column=1)

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(row=2, column=0, columnspan=2)

        def submit():
            try:
                name = name_entry.get()
                rank = float(rank_entry.get())
                self.ranking_list.insert_new_item(name, rank)
                self.refresh_list()
                popup.destroy()
            except ValueError as e:
                error_label.config(text=str(e))

        submit_button = tk.Button(popup, text="Submit", command=submit)
        submit_button.grid(row=3, column=0, columnspan=2)

    def open_tier_list(self):
        popup = tk.Toplevel(self.window)
        popup.title("Tier List")

        tier_list = self.ranking_list.tier_list()
        for tier, items in tier_list.items():
            tk.Label(popup, text=f"{tier}:").pack(anchor="w")
            for item in items:
                tk.Label(popup, text=f"  - {item}").pack(anchor="w")
