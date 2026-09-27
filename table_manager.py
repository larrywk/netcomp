#!/usr/bin/env python3
"""
table_manager.py

A screen-based (Tkinter/Tcl-Tk) program to maintain a table of records with:
    Node          - 8 character field
    Dest          - 8 character field
    Fiber_Length  - integer field
    SRLG          - 8 character field

The (Node, Dest) pair must be unique across the table.

Data is persisted to a local JSON file (table_data.json) in the same
directory as this script, so records survive between runs.

Run with:
    python3 table_manager.py
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
FIELD_MAX_LEN = 8
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spans.json")

COLUMNS = ("Node", "Dest", "Fiber_Length", "SRLG")


class TableManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Table Manager - Node / Dest / Fiber_Length / SRLG")
        self.root.geometry("720x480")
        self.root.minsize(640, 420)

        # In-memory record store: list of dicts
        self.records = []

        # Tracks the (Node, Dest) key of the row currently selected/loaded
        # into the entry fields, so "Update" knows which record to replace.
        self.selected_key = None

        self._build_form()
        self._build_table()
        self._build_buttons()
        self._build_status_bar()

        self.load_data()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_form(self):
        form = ttk.LabelFrame(self.root, text="Record")
        form.pack(fill="x", padx=10, pady=(10, 5))

        # Validation command for the 8-char text fields
        vcmd8 = (self.root.register(self._validate_len8), "%P")
        vcmd_int = (self.root.register(self._validate_int), "%P")

        # Node
        ttk.Label(form, text="Node (8 chars):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.node_var = tk.StringVar()
        self.node_entry = ttk.Entry(
            form, textvariable=self.node_var, width=12,
            validate="key", validatecommand=vcmd8
        )
        self.node_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Dest
        ttk.Label(form, text="Dest (8 chars):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.dest_var = tk.StringVar()
        self.dest_entry = ttk.Entry(
            form, textvariable=self.dest_var, width=12,
            validate="key", validatecommand=vcmd8
        )
        self.dest_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Fiber_Length
        ttk.Label(form, text="Fiber Length (int):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.fiber_length_var = tk.StringVar()
        self.fiber_length_entry = ttk.Entry(
            form, textvariable=self.fiber_length_var, width=12,
            validate="key", validatecommand=vcmd_int
        )
        self.fiber_length_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # SRLG
        ttk.Label(form, text="SRLG (8 chars):").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.srlg_var = tk.StringVar()
        self.srlg_entry = ttk.Entry(
            form, textvariable=self.srlg_var, width=12,
            validate="key", validatecommand=vcmd8
        )
        self.srlg_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    def _build_table(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(frame, columns=COLUMNS, show="headings", selectmode="browse")
        for col in COLUMNS:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_by(c))
            width = 100 if col != "Fiber_Length" else 100
            self.tree.column(col, width=width, anchor="center")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)
        self._sort_reverse = {}

    def _build_buttons(self):
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Add", command=self.add_record).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Update", command=self.update_record).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Delete", command=self.delete_record).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Save", command=self.save_data).pack(side="right", padx=4)
        ttk.Button(btn_frame, text="Reload", command=self.load_data).pack(side="right", padx=4)
        ttk.Button(btn_frame, text="Quit Without Saving", command=self.quit_without_saving).pack(side="right", padx=4)

    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="Ready.")
        status = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status.pack(fill="x", side="bottom")

    # ------------------------------------------------------------------
    # Field validation (live, as user types)
    # ------------------------------------------------------------------
    def _validate_len8(self, proposed_value):
        return len(proposed_value) <= FIELD_MAX_LEN

    def _validate_int(self, proposed_value):
        if proposed_value == "":
            return True
        if len(proposed_value) > 8:
            return False
        return proposed_value.lstrip("-").isdigit() or proposed_value == "-"

    # ------------------------------------------------------------------
    # Form <-> record helpers
    # ------------------------------------------------------------------
    def _read_form(self):
        """Read and validate the form; returns a record dict or None (with
        an error message shown) if invalid."""
        node_val = self.node_var.get().strip()
        dest_val = self.dest_var.get().strip()
        fiber_length_val = self.fiber_length_var.get().strip()
        srlg_val = self.srlg_var.get().strip()

        if not node_val or not dest_val:
            messagebox.showerror("Validation Error", "'Node' and 'Dest' fields are required.")
            return None
        if len(node_val) > FIELD_MAX_LEN or len(dest_val) > FIELD_MAX_LEN or len(srlg_val) > FIELD_MAX_LEN:
            messagebox.showerror(
                "Validation Error",
                f"'Node', 'Dest', and 'SRLG' must be at most {FIELD_MAX_LEN} characters."
            )
            return None
        if not fiber_length_val:
            messagebox.showerror("Validation Error", "'Fiber_Length' is required.")
            return None
        try:
            fiber_length_int = int(fiber_length_val)
        except ValueError:
            messagebox.showerror("Validation Error", "'Fiber_Length' must be an integer.")
            return None

        return {"node": node_val, "dest": dest_val, "fiber_length": fiber_length_int, "srlg": srlg_val}

    def clear_form(self):
        self.node_var.set("")
        self.dest_var.set("")
        self.fiber_length_var.set("")
        self.srlg_var.set("")
        self.selected_key = None
        self.tree.selection_remove(self.tree.selection())
        self.status_var.set("Form cleared.")

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------
    def _find_index(self, node_val, dest_val):
        for i, rec in enumerate(self.records):
            if rec["node"] == node_val and rec["dest"] == dest_val:
                return i
        return -1

    def add_record(self):
        rec = self._read_form()
        if rec is None:
            return
        if self._find_index(rec["node"], rec["dest"]) != -1:
            messagebox.showerror(
                "Duplicate Entry",
                f"A record with Node='{rec['node']}' and Dest='{rec['dest']}' already exists.\n"
                "The (Node, Dest) pair must be unique."
            )
            return
        self.records.append(rec)
        self._refresh_table()
        self.status_var.set(f"Added record {rec['node']} -> {rec['dest']}.")
        self.clear_form()

    def update_record(self):
        if self.selected_key is None:
            messagebox.showerror("No Selection", "Select a row in the table to update, then click Update.")
            return
        rec = self._read_form()
        if rec is None:
            return

        old_node, old_dest = self.selected_key
        old_index = self._find_index(old_node, old_dest)
        if old_index == -1:
            messagebox.showerror("Error", "Original record no longer exists.")
            return

        # If the (Node, Dest) pair changed, make sure the new pair isn't
        # already used by a *different* record.
        if (rec["node"], rec["dest"]) != (old_node, old_dest):
            conflict_index = self._find_index(rec["node"], rec["dest"])
            if conflict_index != -1:
                messagebox.showerror(
                    "Duplicate Entry",
                    f"A record with Node='{rec['node']}' and Dest='{rec['dest']}' already exists.\n"
                    "The (Node, Dest) pair must be unique."
                )
                return

        self.records[old_index] = rec
        self._refresh_table()
        self.status_var.set(f"Updated record {rec['node']} -> {rec['dest']}.")
        self.clear_form()

    def delete_record(self):
        if self.selected_key is None:
            messagebox.showerror("No Selection", "Select a row in the table to delete.")
            return
        node_val, dest_val = self.selected_key
        index = self._find_index(node_val, dest_val)
        if index == -1:
            messagebox.showerror("Error", "Record no longer exists.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Delete record {node_val} -> {dest_val}?"):
            return
        del self.records[index]
        self._refresh_table()
        self.status_var.set(f"Deleted record {node_val} -> {dest_val}.")
        self.clear_form()

    # ------------------------------------------------------------------
    # Table / selection handling
    # ------------------------------------------------------------------
    def _refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        for rec in self.records:
            self.tree.insert(
                "", "end",
                iid=f"{rec['node']}\x1f{rec['dest']}",  # unique row id from the key
                values=(rec["node"], rec["dest"], rec["fiber_length"], rec["srlg"])
            )
        self.status_var.set(f"{len(self.records)} record(s).")

    def _on_row_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection[0], "values")
        node_val, dest_val, fiber_length_val, srlg_val = values
        self.node_var.set(node_val)
        self.dest_var.set(dest_val)
        self.fiber_length_var.set(str(fiber_length_val))
        self.srlg_var.set(srlg_val)
        self.selected_key = (node_val, dest_val)

    def _sort_by(self, col):
        reverse = self._sort_reverse.get(col, False)
        key_func = (lambda r: r["Fiber_Length"]) if col == "Fiber_Length" else (lambda r: r[col])
        self.records.sort(key=key_func, reverse=reverse)
        self._sort_reverse[col] = not reverse
        self._refresh_table()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def save_data(self):
        # Keep the saved file (and the on-screen table) sorted by Node, then Dest.
        self.records.sort(key=lambda r: (r["node"], r["dest"]))
        self._refresh_table()
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.records, f, indent=2)
            self.status_var.set(f"Saved {len(self.records)} record(s) to {DATA_FILE} (sorted by Node, Dest).")
        except OSError as e:
            messagebox.showerror("Save Error", f"Could not save data:\n{e}")

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            self.records = []
            self._refresh_table()
            self.status_var.set("No existing data file found. Starting with an empty table.")
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.records = json.load(f)
            self._refresh_table()
            self.status_var.set(f"Loaded {len(self.records)} record(s) from {DATA_FILE}.")
        except (OSError, json.JSONDecodeError) as e:
            messagebox.showerror("Load Error", f"Could not load data:\n{e}")
            self.records = []
            self._refresh_table()

    def on_close(self):
        self.save_data()
        self.root.destroy()

    def quit_without_saving(self):
        if messagebox.askyesno(
            "Quit Without Saving",
            "Quit without saving? Any changes since the last save will be lost."
        ):
            self.root.destroy()


def main():
    root = tk.Tk()
    app = TableManagerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
