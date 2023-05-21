# -*- coding: utf-8 -*-

# Python 3.7 Larry Weeks

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

def close_app():
   
    root.destroy()
        
    
def askscriptname(self):
    global scriptname
    scriptname =  filedialog.askopenfilename(initialdir =\
                   workingdir,title = \
                "Select Scriptfile",filetypes = \
                    (("text files","*.txt"),("all files","*.*")))
    
   
    
class Application(tk.Frame):
    
    def _init_(self):
        print("Null Init")
     #   self.master=master
        
        
        #Application.buildscreen(self)
        
    def saveasfile():
        global blob
        
        app.newscriptname =  filedialog.asksaveasfilename(initialdir = workingdir,\
                                       title = \
            "Select Output Scriptfile",filetypes = \
                (("text files","new*.txt"),("all files","*.*")))
        if app.newscriptname and app.newscriptname.find(".txt") < 1:
            app.newscriptname=app.newscriptname+".txt"
            # Make sure windows knows this is a txt file
        if app.newscriptname :         
            f=open(app.newscriptname,"w")
            f.write(blob)
            f.close 
        else:
            tk.messagebox.showwarning("warning","File not saved")
        
    def buildscreen(self):
        
            
        def subvars():
            global blob
            sellist=self.listbox.get(0,tk.END)
            replist=self.valbox.get(0,tk.END)
            ix =0
            for var in sellist:
                repvalue=replist[ix]
                blob=blob.replace(var,repvalue)
                ix = ix +1
            self.textbox.delete("1.0",tk.END)
            self.textbox.insert("1.0",blob)
            #self.textbox.insert("1.0","This is the new text")
            self.textbox.grid()
            findvars()
            
            
        global foundat
        foundat=tk.Label(frame1,text=" Variables Found List")  
        foundat.grid(row=1,column=0)
        
            
        self.QUIT = tk.Button(frame2)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  close_app
        self.QUIT.grid(row=1,column=5,sticky="ew")
        
        self.curdir = tk.Label(frame2)
        self.curdir["text"]=os.path.realpath(f.name)
        self.curdir.grid(sticky="ew")
        
        self.findthem=tk.Button(frame2)
        self.findthem["text"]=" Find vars "
        self.findthem.grid(sticky="w")
        self.findthem["command"]=findvars  
        
        self.subbutton=tk.Button(frame2)
        self.subbutton["text"]="Do Substitutions"
        self.subbutton.grid(sticky="w")
        self.subbutton["command"]=subvars
        
        self.button=tk.Button(frame2)
        self.button["text"]=" Save File "
        self.button["command"]=Application.saveasfile
        self.button.grid(sticky="w")
        
        self.spacer1 = tk.Label(frame2,text="  ")
        self.spacer1.grid()
        
        self.textbox=tk.Text(frame3,width=100,height=20)
        self.textbox.grid(column=0,row=1)
        self.textbox.insert("1.0",blob)
        self.scrolltext = tk.Scrollbar(frame3,orient="vertical")
        self.scrolltext.grid(column=0,row=1,sticky="ens")
        self.scrolltext.config(command = self.textbox.yview)
        self.textbox.configure(yscrollcommand=self.scrolltext.set)
        
        self.listbox=tk.Listbox(frame2,width=20,height=8)
        self.scrollbox = tk.Scrollbar(frame2, orient="vertical")

        self.listbox.grid(row=3,column=1,rowspan=2,columnspan=2,sticky="w")
        self.scrollbox.grid(row=3,column=2,rowspan=2,sticky="ens")
        self.scrollbox.config( command = self.listbox.yview )
        self.listbox.configure(yscrollcommand=self.scrollbox.set)
        
        self.valbox=tk.Listbox(frame2,width=30,height=8)
        self.scrollval= tk.Scrollbar(frame2, orient="vertical")
        self.valbox.grid(row=3,column=3,rowspan=2,columnspan=2,sticky="w")
        self.scrollval.grid(row=3,column=4,rowspan=2,sticky="ens")
        self.valbox.configure(yscrollcommand=self.scrollval.set)
        
        for each in allofthem.split("\n"):
            if len(each.split(",")) < 2: break
            var,repvalue=each.split(",")
            sellist.append(var)
            replist.append(repvalue)
            self.listbox.insert(tk.END,var)
            self.valbox.insert(tk.END,repvalue)
      
      
def findvars():
    global blob
    global foundat
    ix = 1
    displaytext=" $ found at \n"
    savedisplaytext=displaytext
    while blob.find("$",ix,len(blob)) > 0:
         ix = blob.find("$",ix,len(blob))
         linenum=len(blob[0:ix].splitlines())
         displaytext=displaytext+" found on line "+str(linenum)+"\n"
         ix = ix + 1
    if displaytext == savedisplaytext : displaytext = "  None remaining"
    foundat["text"]=displaytext
    foundat.grid()
      
#--------  Start of main code -----------------------------------------
root=tk.Tk()
root.geometry('960x640+50+50')
root.title("Replace variable in script")

frame1=tk.Frame(root)
frame1.grid(column=1,row=1)
frame2=tk.Frame(root)
frame2.grid(column=2,row=2)
frame3=tk.Frame(root)
frame3.grid(column=2,row=4)

global workingdir

workingdir="/home/larry/work"
#workingdir ="S:\GIO\PUBLIC\DEVTOOLS"   Find some share drive directory
askscriptname(root)

if scriptname :  # Ifthey hit cancel then abort the program
    f=open(scriptname,"r")   # Read in template
else:
    root.destroy()
    os.sys.exit()
    
global blob
blob=f.read()
f.close()

valpairsname =  filedialog.askopenfilename(initialdir = workingdir,\
                                        title = \
             "Value Pairs File",filetypes = \
                 (("csv files","*.csv"),("all files","*.*")))
try:
    f=open(valpairsname,"r")
    allofthem=f.read()
    f.close
except OSError as e:
    print("Couldn't open valpairs file", str(e))
    root.destroy()
    os.sys.exit()
    
sellist=[]
replist=[]



app=Application(root)

Application.buildscreen(root)  # still don't know why _init_ is not called
 
app.mainloop()

