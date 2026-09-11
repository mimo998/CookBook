import tkinter as tk


class TryLaterFrame(tk.Frame):
    def __init__(self, parent, try_later_list, ranking_list, show_home):
        super().__init__(parent)
        self.try_later_list = try_later_list
        self.ranking_list = ranking_list

        header = tk.Frame(self)
        header.pack(fill="x", padx=10, pady=(10, 4))
        tk.Button(header, text="\u2190 Back", command=show_home).pack(side="left")
        tk.Label(header, text="Try Later", font=("Segoe UI", 14, "bold")).pack(side="left", padx=12)

        body = tk.Frame(self)
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        button_frame = tk.Frame(body)
        button_frame.pack(side="left", fill="y", padx=(0, 8))

        for text, command in [
            ("Add", self.open_add_popup),
            ("Delete", self.delete_selected),
            ("Move to Ranking", self.open_move_popup),
        ]:
            tk.Button(button_frame, text=text, width=14, command=command).pack(fill="x", pady=2)

        self.listbox = tk.Listbox(body, font=("Consolas", 11))
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(body, command=self.listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for name in self.try_later_list.get_items():
            self.listbox.insert(tk.END, name)

    def _selected_name(self):
        selection = self.listbox.curselection()
        if not selection:
            return None
        return self.listbox.get(selection[0])

    def delete_selected(self):
        name = self._selected_name()
        if name is None:
            return
        self.try_later_list.remove_item(name)
        self.refresh_list()

    def open_add_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add to Try Later")
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        tk.Label(popup, text="Name:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1, padx=6, pady=6)

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(row=1, column=0, columnspan=2)

        def submit():
            try:
                self.try_later_list.add_item(name_entry.get())
                self.refresh_list()
                popup.destroy()
            except ValueError as e:
                error_label.config(text=str(e))

        tk.Button(popup, text="Submit", command=submit).grid(row=2, column=0, columnspan=2, pady=(0, 8))

    def open_move_popup(self):
        name = self._selected_name()
        if name is None:
            return

        popup = tk.Toplevel(self)
        popup.title("Move to Ranking")
        popup.transient(self.winfo_toplevel())
        popup.grab_set()

        tk.Label(popup, text=f"Rank for '{name}' (0-10):").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        rank_entry = tk.Entry(popup)
        rank_entry.grid(row=0, column=1, padx=6, pady=6)

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(row=1, column=0, columnspan=2)

        def submit():
            try:
                rank = float(rank_entry.get())
                self.ranking_list.insert_new_item(name, rank)   # do this first
                self.try_later_list.remove_item(name)           # only remove once the move succeeded
                self.refresh_list()
                popup.destroy()
            except ValueError as e:
                error_label.config(text=str(e))

        tk.Button(popup, text="Submit", command=submit).grid(row=2, column=0, columnspan=2, pady=(0, 8))
