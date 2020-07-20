#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:00:33 2020

@author: larry
"""


import tkinter as tk
import os

class Application(tk.Frame):
    
    

    def buildscreen(self):
        
        def close_app():
            root.destroy()
            
        def run_replacevars():
            os.system("python replacevars.py")

            
        def run_askpath():
            os.system("python askpath.py")
            
        def run_diversepath():
            os.system("python diversefrom.py")
            
        
        self.QUIT = tk.Button(frame2)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  close_app
        self.QUIT.grid(row=1,column=5,sticky="ew")
        
        self.spacer1=tk.Label(frame2,text=" ")
        self.spacer1.grid(row=2,rowspan=2)
    
        self.button=tk.Button(frame2)
        self.button["text"]="Replace Variables in a script file"
        self.button["command"]=run_replacevars
        self.button.grid(row=4)
        
        self.askpath=tk.Button(frame2)
        self.askpath["text"]="Run MTBF Computation"
        self.askpath["command"]=run_askpath
        self.askpath.grid(row=5)
        
        self.diversepath=tk.Button(frame2, \
                                   text=" Run Diverse Path Computation")
        self.diversepath["command"]=run_diversepath
        self.diversepath.grid(row=6)
        
        self.spacer=tk.Label(frame3,text=" ")
        self.spacer.grid(row=1,rowspan=2)
        
        mydir="Working in "+os.getcwd()
        self.whereami=tk.Label(frame2,text=mydir)
        self.whereami.grid()
        
        global blob
        self.instructions = tk.Label(frame3,text=blob)
        self.instructions.grid(row=3,sticky="w")
        
       
        
root=tk.Tk()
root.geometry('960x640+0+0')
root.title("Menu of Network Design Aids")


frame1=tk.Frame(root)
frame1.grid(column=1,row=1)
frame2=tk.Frame(root)
frame2.grid(column=2,row=2)
frame3=tk.Frame(root)
frame3.grid(column=2,row=4)

f=open("replacevars_instructions.txt","r")   # Read in template
global blob
blob=f.read()
f.close()


app=Application()

Application.buildscreen(root)  # still don't know why _init_ is not called
 
app.mainloop()