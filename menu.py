#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:00:33 2020
Rewritten for clarity and portability.

@author: larry
"""

import sys
import os
import tkinter as tk


INSTRUCTIONS_FILE = "replacevars_instructions.txt"


class Application(tk.Frame):
    """Main menu GUI for the Network Design Aids toolkit."""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.instructions_text = self._load_instructions()

        self.frame1 = tk.Frame(master)
        self.frame1.grid(column=1, row=1)
        self.frame2 = tk.Frame(master)
        self.frame2.grid(column=2, row=2)
        self.frame3 = tk.Frame(master)
        self.frame3.grid(column=2, row=4)

        self.buildscreen()

    def _load_instructions(self):
        """Read the instructions file, falling back gracefully if missing."""
        try:
            with open(INSTRUCTIONS_FILE, "r") as f:
                return f.read()
        except FileNotFoundError:
            return (
                f"[{INSTRUCTIONS_FILE} not found in {os.getcwd()} "
                "- run this app from the repo root]"
            )

    @staticmethod
    def _run_script(script_name):
        """Run a helper script using the same Python interpreter as this app."""
        os.system(f'"{sys.executable}" {script_name}')

    def buildscreen(self):
        def close_app():
            self.master.destroy()

        def run_replacevars():
            self._run_script("replacevars.py")

        def run_askpath():
            self._run_script("askpath.py")

        def run_diversepath():
            self._run_script("diversefrom.py")

        self.quit_button = tk.Button(
            self.frame2, text="QUIT", fg="red", command=close_app
        )
        self.quit_button.grid(row=1, column=5, sticky="ew")

        self.spacer1 = tk.Label(self.frame2, text=" ")
        self.spacer1.grid(row=2, rowspan=2)

        self.replacevars_button = tk.Button(
            self.frame2,
            text="Replace Variables in a script file",
            command=run_replacevars,
        )
        self.replacevars_button.grid(row=4)

        self.askpath_button = tk.Button(
            self.frame2,
            text="Run MTBF Computation",
            command=run_askpath,
        )
        self.askpath_button.grid(row=5)

        self.diversepath_button = tk.Button(
            self.frame2,
            text=" Run Diverse Path Computation",
            command=run_diversepath,
        )
        self.diversepath_button.grid(row=6)

        self.spacer2 = tk.Label(self.frame3, text=" ")
        self.spacer2.grid(row=1, rowspan=2)

        mydir = "Working in " + os.getcwd()
        self.whereami = tk.Label(self.frame2, text=mydir)
        self.whereami.grid()

        self.instructions = tk.Label(self.frame3, text=self.instructions_text)
        self.instructions.grid(row=3, sticky="w")


def main():
    root = tk.Tk()
    root.geometry("960x640+0+0")
    root.title("Menu of Network Design Aids")

    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
