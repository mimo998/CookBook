import tkinter as tk


class TryLaterWindow:
    def __init__(self, root, try_later_list, ranking_list):
        self.try_later_list = try_later_list
        self.ranking_list = ranking_list

        self.window = tk.Toplevel(root)
        self.window.title("Try Later")

        button_frame = tk.Frame(self.window)
        button_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.add_button = tk.Button(button_frame, text="Add", command=self.open_add_popup)
        self.add_button.pack(fill="x")

        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_selected)
        self.delete_button.pack(fill="x")

        self.move_button = tk.Button(button_frame, text="Move to Ranking", command=self.open_move_popup)
        self.move_button.pack(fill="x")

        self.listbox = tk.Listbox(self.window, width=40)
        self.listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for name in self.try_later_list.get_items():
            self.listbox.insert(tk.END, name)

    def delete_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        name = self.listbox.get(selection[0])
        self.try_later_list.remove_item(name)
        self.refresh_list()

    def open_add_popup(self):
        popup = tk.Toplevel(self.window)
        popup.title("Add to Try Later")

        tk.Label(popup, text="Name:").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1)

        self.error_label = tk.Label(popup, text="", fg="red")
        self.error_label.grid(row=1, column=0, columnspan=2)

        def submit():
            try:
                self.try_later_list.add_item(name_entry.get())
                self.refresh_list()
                popup.destroy()
            except ValueError as e:
                self.error_label.config(text=str(e))

        submit_button = tk.Button(popup, text="Submit", command=submit)
        submit_button.grid(row=2, column=0, columnspan=2)

    def open_move_popup(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        name = self.listbox.get(selection[0])

        popup = tk.Toplevel(self.window)
        popup.title("Move to Ranking")

        tk.Label(popup, text="Rank (0-10):").grid(row=0, column=0, sticky="e")
        rank_entry = tk.Entry(popup)
        rank_entry.grid(row=0, column=1)

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(row=1, column=0, columnspan=2)

        def submit():
            try:
                rank = float(rank_entry.get())
                self.ranking_list.insert_new_item(name, rank)   # do this first
                self.try_later_list.remove_item(name)            # only remove once the move succeeded
                self.refresh_list()
                popup.destroy()
            except ValueError as e:
                error_label.config(text=str(e))

        submit_button = tk.Button(popup, text="Submit", command=submit)
        submit_button.grid(row=2, column=0, columnspan=2)
