#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 15:57:27 2020

@author: larry
"""


import tkinter as Tk

import sys

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.grid()
        self.createWidgets()
    def createWidgets(self):
        self.quitButton = Tk.Button(text='Quit',command=self.destroy) # Use destroy instead of quit
        self.quitButton.grid()

app = Application()
app.title("Sample application")
app.mainloop()