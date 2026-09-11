import tkinter as tk


class RestaurantsFrame(tk.Frame):
    def __init__(self, parent, restaurants_list, show_home):
        super().__init__(parent)
        self.restaurants_list = restaurants_list

        header = tk.Frame(self)
        header.pack(fill="x", padx=10, pady=(10, 4))
        tk.Button(header, text="\u2190 Back", command=show_home).pack(side="left")
        tk.Label(header, text="Restaurants", font=("Segoe UI", 14, "bold")).pack(side="left", padx=12)

        body = tk.Frame(self)
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        button_frame = tk.Frame(body)
        button_frame.pack(side="left", fill="y", padx=(0, 8))

        for text, command in [
            ("Add", self.open_add_popup),
            ("Edit", self.open_edit_popup),
            ("Delete", self.delete_selected),
        ]:
            tk.Button(button_frame, text=text, width=12, command=command).pack(fill="x", pady=2)

        self.listbox = tk.Listbox(body, font=("Consolas", 11))
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(body, command=self.listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for name, rank in self.restaurants_list.ranking_sort().items():
            self.listbox.insert(tk.END, f"{rank:>5.1f}   {name}")

    def _selected_name(self):
        selection = self.listbox.curselection()
        if not selection:
            return None
        return self.listbox.get(selection[0]).split(maxsplit=1)[1]

    def delete_selected(self):
        name = self._selected_name()
        if name is None:
            return
        self.restaurants_list.remove_restaurant(name)
        self.refresh_list()

    def open_edit_popup(self):
        name = self._selected_name()
        if name is None:
            return

        popup = tk.Toplevel(self)
        popup.title("Edit Restaurant Rank")
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        tk.Label(popup, text="New Rank (0-5):").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        rank_entry = tk.Entry(popup)
        rank_entry.grid(row=0, column=1, padx=6, pady=6)

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(row=1, column=0, columnspan=2)

        def submit():
            try:
                self.restaurants_list.change_restaurant_rank(name, float(rank_entry.get()))
                self.refresh_list()
                popup.destroy()
            except ValueError as e:
                error_label.config(text=str(e))

        tk.Button(popup, text="Submit", command=submit).grid(row=2, column=0, columnspan=2, pady=(0, 8))

    def open_add_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add Restaurant")
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        tk.Label(popup, text="Name:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1, padx=6, pady=6)

        tk.Label(popup, text="Rank (0-5):").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        rank_entry = tk.Entry(popup)
        rank_entry.grid(row=1, column=1, padx=6, pady=6)

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(row=2, column=0, columnspan=2)

        def submit():
            try:
                self.restaurants_list.add_restaurant(name_entry.get(), float(rank_entry.get()))
                self.refresh_list()
                popup.destroy()
            except ValueError as e:
                error_label.config(text=str(e))

        tk.Button(popup, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=(0, 8))
