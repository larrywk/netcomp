"""
diversefrom.py

GUI application to select FROM and TO nodes from a fiber network topology
and compute the shortest path between them that avoids a chosen set of
Shared Risk Link Groups (SRLGs).

Refactored from the original by Larry Weeks (Python 3.7).

Key changes from the original:
  - Graph/path-finding logic is isolated in NetworkGraph, independent of
    Tkinter, so it can be tested or reused without building the GUI.
  - No module-level globals; state lives on NetworkGraph and Application
    instances.
  - Fixed a latent bug where button-handler methods and label widgets
    shared the same attribute name (self.frm_node / self.to_node),
    which only worked by accident of execution order.
  - Span data is loaded from a JSON file instead of a CSV file (see
    NetworkGraph docstring for the expected format).
  - Missing/malformed input files produce a friendly error dialog
    instead of crashing with a raw traceback.
  - Results are built as a string in memory and shown directly in the
    Text widget, instead of writing a file and immediately reopening it
    to redisplay it. A "Save Results" button lets the user save the
    most recent report to a file on demand, rather than a file being
    written automatically after every compute.
  - Path search does an early-exit avoid-list check while walking the
    graph, rather than generating full candidate paths and separately
    re-walking each one to compute its length.
"""

import os
import sys
import json
from datetime import datetime

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

SPANS_FILE = "spans.json"
AVOID_FILE = "srlglist.csv"


# --------------------------------------------------------------------------
# Graph model / path finding (no Tkinter dependency)
# --------------------------------------------------------------------------

class NetworkGraph:
    """Loads span data from a JSON file and finds SRLG-diverse shortest paths.

    spans.json format: a JSON array of span objects, e.g.

        [
          {"Node": "A", "Dest": "B", "Fiber_Length": 12.5, "SRLG": "1"},
          {"Node": "B", "Dest": "A", "Fiber_Length": 12.5, "SRLG": "1"},
          ...
        ]

    Each object must have "Node", "Dest", "Fiber_Length" and "SRLG" keys
    (this mirrors the original spans.csv columns: node,dest,fiber_length,srlg).
    Spans are directional, so a bidirectional link needs two entries, one
    in each direction, same as the original CSV format.
    """

    def __init__(self, spans_file=SPANS_FILE):
        self.spans_file = spans_file
        self.graph = {}        # node -> list of neighbor nodes
        self.span_index = {}   # "from,to" -> row index
        self.fiber_len = []    # index -> length (float)
        self.srlg = []         # index -> srlg id (str)
        self._load()

    def _load(self):
        if not os.path.exists(self.spans_file):
            raise FileNotFoundError(f"{self.spans_file} not found")

        with open(self.spans_file, "r") as f:
            try:
                records = json.load(f)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"{self.spans_file} is not valid JSON: {exc}"
                ) from exc

        if not isinstance(records, list):
            raise ValueError(
                f"{self.spans_file} must contain a JSON array of span objects"
            )

        required_keys = ("node", "dest", "fiber_length", "srlg")
        for lineix, record in enumerate(records):
            if not isinstance(record, dict):
                raise ValueError(
                    f"Entry {lineix} in {self.spans_file} is not an object: "
                    f"{record!r}"
                )
            missing = [k for k in required_keys if k not in record]
            if missing:
                raise ValueError(
                    f"Entry {lineix} in {self.spans_file} is missing "
                    f"{missing}: {record!r}"
                )

            node = str(record["node"]).strip()
            dest = str(record["dest"]).strip()
            spansrlg = str(record["srlg"]).strip()
            fiberlength = record["fiber_length"]
            fromto = f"{node},{dest}"

            self.span_index[fromto] = lineix
            try:
                self.fiber_len.append(float(fiberlength))
            except (TypeError, ValueError):
                raise ValueError(
                    f"Bad fiber_length on entry {lineix} of "
                    f"{self.spans_file}: {fiberlength!r}"
                )
            self.srlg.append(spansrlg)

            neighbors = self.graph.setdefault(node, [])
            if dest in neighbors:
                messagebox.showwarning("Warning", f"{dest} already in {node}")
            else:
                neighbors.append(dest)

    def nodes(self):
        return sorted(self.graph.keys())

    def srlgs(self):
        def sort_key(s):
            # Sort numerically when possible so SRLG "2" comes before "10".
            return (0, int(s)) if s.isdigit() else (1, s)
        return sorted(set(self.srlg), key=sort_key)

    def path_length(self, path, avoid):
        """Total length of path, or 0 if empty / crosses an avoided SRLG."""
        if not path or len(path) < 2:
            return 0
        total = 0.0
        for a, b in zip(path, path[1:]):
            ix = self.span_index.get(f"{a},{b}")
            if ix is None:
                return 0
            if self.srlg[ix] in avoid:
                return 0
            total += self.fiber_len[ix]
        return total

    def find_shortest_path(self, start, end, avoid):
        """DFS for the shortest simple path start->end avoiding given SRLGs.

        Prunes branches as soon as they cross an avoided SRLG, rather than
        generating whole candidate paths and rejecting them afterward.
        Suitable for small/medium topologies (this is not Dijkstra; for
        large graphs a proper shortest-path algorithm would be faster).
        """
        if start not in self.graph:
            return None

        best_path = None
        best_len = None

        def visit(node, path, length_so_far):
            nonlocal best_path, best_len
            if node == end:
                if best_len is None or length_so_far < best_len:
                    best_path, best_len = list(path), length_so_far
                return
            if best_len is not None and length_so_far >= best_len:
                return  # already worse than the best found so far
            for nxt in self.graph.get(node, []):
                if nxt in path:
                    continue
                ix = self.span_index.get(f"{node},{nxt}")
                if ix is None or self.srlg[ix] in avoid:
                    continue
                path.append(nxt)
                visit(nxt, path, length_so_far + self.fiber_len[ix])
                path.pop()

        visit(start, [start], 0.0)
        return best_path

    def describe_path(self, start, end, path, avoid):
        """Build a human-readable results report and the list of SRLGs used.

        Returns (report_text, srlgs_used_sorted).
        """
        lines = []
        if avoid:
            lines.append("Avoiding " + str(sorted(avoid)))
        lines.append(f"Looking for {start} to {end}")
        lines.append(str(path))

        srlgs_used = []
        if path:
            lines.append("             Span       Total")
            lines.append("Node         Length     Length  SRLG  IX")
            total = 0
            for i, node in enumerate(path):
                line = f"{node:<8}"
                if i > 0:
                    ix = self.span_index[f"{path[i - 1]},{node}"]
                    length = int(self.fiber_len[ix])
                    spansrlg = self.srlg[ix]
                    total += length
                    line += f"{length:,}".rjust(11)
                    line += f"{total:,}".rjust(11)
                    line += f"  {spansrlg} {ix}"
                    if spansrlg not in srlgs_used:
                        srlgs_used.append(spansrlg)
                lines.append(line)
        else:
            lines.append("No path found.")

        def sort_key(s):
            return (0, int(s)) if s.isdigit() else (1, s)

        return "\n".join(lines), sorted(srlgs_used, key=sort_key)


def load_avoid_list(fname=AVOID_FILE):
    """Load a saved list of SRLGs to avoid, if the file exists."""
    if not os.path.exists(fname):
        return []
    with open(fname, "r") as f:
        return [line.strip() for line in f if line.strip()]


def save_avoid_list(avoid_list, fname=AVOID_FILE):
    with open(fname, "w") as f:
        for srlg in avoid_list:
            f.write(srlg + "\n")


# --------------------------------------------------------------------------
# GUI
# --------------------------------------------------------------------------

class Application(tk.Frame):
    def __init__(self, master, network):
        global search_text
        super().__init__(master, bg="red")
        self.master = master
        self.network = network

        self.from_node = None
        self.to_node = None
        self.avoid_list = load_avoid_list()
        self.search_text = ""
        self.last_report = None  # results text from the most recent compute

        self.grid(row=0, column=1)
        self._build_widgets()

    # -- widget construction ------------------------------------------------

    def _build_widgets(self):
        root = self.master

        # Quit button
        quit_btn = tk.Button(root, text="QUIT", fg="red", command=self._on_quit)
        quit_btn.grid(row=1, column=5, sticky="ew", padx=4, pady=4)

        # Instructions
        tk.Label(
            root, width=28,
            text=" Highlight a node and then\n"
                 "select FROM and TO \n then click Compute Path",
        ).grid(row=2, column=3, padx=20, columnspan=2)

        tk.Label(root, text="Node List:   SRLG List:").grid(
            row=2, column=1, sticky="sw"
        )

        # From / To selection buttons + status labels
        tk.Button(
            root, text="Select FROM Node", command=self._on_select_from
        ).grid(row=3, column=3, sticky="ws")

        tk.Button(
            root, text="Select TO node", width=14, command=self._on_select_to
        ).grid(row=4, column=3, sticky="wn")

        self.from_label = tk.Label(root, text="    From", fg="blue")
        self.from_label.grid(row=3, column=2, sticky="es")

        self.to_label = tk.Label(root, text="       To", fg="blue")
        self.to_label.grid(row=4, column=2, sticky="en")

        # Avoid-list controls
        tk.Button(
            root, text="Add AVOID SRLG", command=self._on_add_avoid
        ).grid(row=5, column=3, sticky="w")

        self.clear_avoid_btn = tk.Button(
            root, text="Clear AVOID List", command=self._on_clear_avoid
        )
        self.clear_avoid_btn.grid(row=5, column=5, sticky="ne")
        if not self.avoid_list:
            self.clear_avoid_btn.grid_remove()

        tk.Button(
            root, text="Compute Path", width=14, command=self._on_compute
        ).grid(row=6, column=3, sticky="w")

        tk.Button(
            root, text="Save Results", command=self._on_save_results
        ).grid(row=6, column=4, sticky="w")

        tk.Label(root, text="      Avoid List:").grid(
            row=3, column=4, columnspan=2, sticky="es"
        )

        self.avoid_listbox = tk.Listbox(root, width=12, height=5)
        self.avoid_listbox.grid(row=4, column=4, columnspan=2, sticky="ne")
        for srlg in self.avoid_list:
            self.avoid_listbox.insert(tk.END, srlg)

        # Search-as-you-type field for the node list
        self.search_field = tk.Text(root, height=1, width=12)
        self.search_field.grid(row=4, column=1, columnspan=2, sticky="nw")
        self.search_field.bind("<Key>", self._on_search_key)
        self.search_field.focus_set()

        # Node list (with scrollbar) + SRLG list (with scrollbar)
        list_frame = tk.Frame(master=root, bg="blue", height=120, bd=2)
        list_frame.grid(column=1, row=3)

        self.node_listbox = tk.Listbox(list_frame, width=12, height=10)
        node_scroll = tk.Scrollbar(list_frame, orient="vertical")
        self.node_listbox.grid(row=3, column=1, rowspan=2, columnspan=2, sticky="w")
        node_scroll.grid(row=3, column=2, rowspan=2, sticky="ens")
        node_scroll.config(command=self.node_listbox.yview)
        self.node_listbox.configure(yscrollcommand=node_scroll.set)
        self.node_listbox.bind("<<ListboxSelect>>", self._on_node_click)

        self.srlg_listbox = tk.Listbox(list_frame, width=12, height=8)
        srlg_scroll = tk.Scrollbar(list_frame, orient="vertical")
        self.srlg_listbox.grid(row=3, column=4)
        srlg_scroll.grid(row=3, column=4, sticky="ens")
        self.srlg_listbox.configure(yscrollcommand=srlg_scroll.set)
        srlg_scroll.config(command=self.srlg_listbox.yview)

        # Populate node and SRLG lists
        self.node_list = self.network.nodes()
        for node in self.node_list:
            self.node_listbox.insert(tk.END, node)
        for srlg in self.network.srlgs():
            self.srlg_listbox.insert(tk.END, srlg)

        # Output area
        self.output = tk.Text(root, height=15, width=65)
        self.output.grid(row=7, column=2, columnspan=4)

    # -- event handlers -------------------------------------------------

    def _on_quit(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.master.destroy()

    def _on_node_click(self, _event):
        # Selecting with the mouse should reset the type-to-search buffer.
        self.search_text = ""

    def _on_select_from(self):
        sel = self.node_listbox.curselection()
        if sel:
            self.from_node = self.node_list[sel[0]]
            self.from_label["text"] = self.from_node

    def _on_select_to(self):
        sel = self.node_listbox.curselection()
        if sel:
            self.to_node = self.node_list[sel[0]]
            self.to_label["text"] = self.to_node

    def _on_add_avoid(self):
        sel = self.srlg_listbox.curselection()
        if not sel:
            return
        value = self.srlg_listbox.get(sel[0])
        if value not in self.avoid_list:
            self.avoid_list.append(value)
            self.avoid_listbox.insert(tk.END, value)
        self.clear_avoid_btn.grid(row=5, column=5, sticky="ne")

    def _on_clear_avoid(self):
        save_avoid_list([])  # empty srlglist.csv, matching original behavior
        self.avoid_list = []
        self.avoid_listbox.delete(0, tk.END)
        self.clear_avoid_btn.grid_remove()

    def _on_search_key(self, event):
        # Move the node-list selection to the first entry >= typed text.
        if event.keysym == "BackSpace":
            self.search_text = self.search_text[:-1]
        elif event.char.isprintable():
            self.search_text += event.char.upper()
            self.search_field.text=self.search_text
        else:
            return "break"

        self.node_listbox.select_clear(0, "end")
        ix = 0
        while ix < len(self.node_list) - 1 and self.node_list[ix] < self.search_text:
            ix += 1
        self.node_listbox.select_set(ix)
        self.node_listbox.see(ix)
        return "break"  # keep the Text widget from actually inserting text

    def _on_save_results(self):
        if not self.last_report:
            messagebox.showwarning("Warning", "No results to save yet")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fname = filedialog.asksaveasfilename(
            initialfile=f"result-{timestamp}.txt",
            title="Save Results",
            filetypes=(("text files", "*.txt"), ("all files", "*.*")),
        )
        if not fname:
            return  # user cancelled

        try:
            with open(fname, "w") as f:
                f.write(self.last_report)
        except OSError as exc:
            messagebox.showerror("Error", f"Could not save {fname}: {exc}")
        else:
            messagebox.showinfo("Saved", f"Results saved to {fname}")

    def _on_compute(self):
        if not self.from_node or not self.to_node:
            messagebox.showwarning("Warning", "Please select from and to nodes")
            return

        try:
            path = self.network.find_shortest_path(
                self.from_node, self.to_node, self.avoid_list
            )
            report, srlgs_used = self.network.describe_path(
                self.from_node, self.to_node, path, self.avoid_list
            )
        except Exception as exc:
            messagebox.showerror("Error computing path", str(exc))
            return

        # Show results in the output box.
        self.output.delete("1.0", "end")
        self.output.insert("1.0", report)

        # Remember the report so "Save Results" can write it out on demand,
        # instead of writing a file automatically after every compute.
        self.last_report = report

        # Refresh the avoid list with the new path's SRLGs, same as original.
        self.avoid_list = srlgs_used
        self.avoid_listbox.delete(0, tk.END)
        for srlg in self.avoid_list:
            self.avoid_listbox.insert(tk.END, srlg)
        if self.avoid_list:
            self.clear_avoid_btn.grid(row=5, column=5, sticky="ne")
        else:
            self.clear_avoid_btn.grid_remove()


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main():
    try:
        network = NetworkGraph(SPANS_FILE)
    except (FileNotFoundError, ValueError) as exc:
        # Need a minimal Tk root to show a dialog even though the main
        # app never starts.
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Startup error", str(exc))
        sys.exit(1)

    root = tk.Tk()
    root.title(".                                 Compute Shortest path which avoids SRLGs")
    root.geometry("1000x700+50+50")

    app = Application(root, network)
    root.protocol("WM_DELETE_WINDOW", app._on_quit)

    root.mainloop()


if __name__ == "__main__":
    main()
