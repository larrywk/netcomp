# Python 3.7 by Larry Weeks
# Application to ask to pick from and to nodes from a list
# and then call an application, passing from and to as
# command line paramaters

import tkinter as tk
import os
import json
#import os.path
from datetime import datetime


class Application(tk.Frame):
    
    def callback(ignore):
         if tk.messagebox.askokcancel("Quit", \
                                      "Do you really wish to quit?"):
             root.destroy()
             quit()

    def frm_node(self):
        selval=listbox.curselection()
        if selval:  # If nothing was selected ignore button click
            ix = int(selval[0])
           #print sellist[ix]
            global fromnode
            fromnode=sellist[ix]
            self.frm_node["text"]=fromnode
            
    def to_node(self):
        selval=listbox.curselection()
        if selval:    # If nothing was selected ignore button click
            ix = int(selval[0])
            global tonode
            tonode  =sellist[ix]      
            self.to_node["text"]=tonode
            
    def empty_avoid(self):
        fname=open("avoid.csv","w")
        fname.close() # Empty the avoid node comma seperated values file
        self.clear_avoid.grid_remove() # Remove the button for clearing
        self.avoidit.delete(0,"end") # Delete prior from screen
        global avoidlist
        avoidlist=[]
        
    def add_avoid(self):
        selval=self.listbox.curselection()
        if selval:  # Ignoore button click if nothing selected
            ix=int(selval[0])
            self.avoidit.insert(tk.END,sellist[ix])
            avoidlist.append(sellist[ix])
            self.clear_avoid.grid(row=5,column=5,sticky="e") # Redisplay

    def compute_pth(self):
        if fromnode == "not" or tonode == "not":
            tk.messagebox.showwarning\
                ("Warning","Please select from and to nodes")
            return()
        f=open("avoid.csv","w")
        for each in avoidlist:
            each=each+"\n"
            f.write(each)
        f.close()
        dateTimeObj = datetime.now()

        timestampStr = dateTimeObj.strftime("%Y-%m-%d-%H-%M-%S")
        fname="result-"+timestampStr

        cmd="python runshortest3.py "+fromnode+" "+tonode+" > "+fname

        os.system(cmd) # runs program to find best path between nodes
	     
        f=open(fname,"r")
        buf=f.read()
        f.close()
        
        self.output.delete("1.0","end") # Delete prior from screen
        self.output.insert("1.0",buf)   # Put new output file contents
	                                    # On the screen
        self.clear_avoid.grid(row=5,column=5) # Redisplay if it was hidden
        self.avoidit.delete(0,"end") # Delete prior from screen
       
        f=open("avoid.csv","r")
        buf=f.read()
        avoidlist.clear()
 
        for each in buf.split("\n"):
            avoidlist.append(each)
            self.avoidit.insert(tk.END,each)
            #print("adding=",each)        
            

    def createWidgets(self):
        self.QUIT = tk.Button(root)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(row=1,column=5,sticky="ew")


        self.from_node = tk.Button(root)
        self.from_node["text"] = "Select FROM Node"
        self.from_node["command"] = self.frm_node
        self.from_node.grid(row=3,column=3,sticky="ws")

        self.sel_to_node  = tk.Button(root)
        self.sel_to_node["text"] = "Select TO node"
        self.sel_to_node["width"]=14
        self.sel_to_node ["command"] = self.to_node
        self.sel_to_node.grid(row=4,column=3,sticky="w")
        
        self.addavoid = tk.Button(root)
        self.addavoid["text"]="Add AVOID Node"
        self.addavoid["command"]=self.add_avoid
        self.addavoid.grid(row=5,column=3,sticky="w")

        self.clear_avoid = tk.Button(root)
        self.clear_avoid["text"] = "Clear AVOID List"
        self.clear_avoid["command"] = self.empty_avoid
        self.clear_avoid.grid(row=5,column=5,sticky="ne")

        self.compute_path = tk.Button(root)
        self.compute_path["text"] = "Compute Path"
        self.compute_path["width"]=14
        self.compute_path["command"] = self.compute_pth
        self.compute_path.grid(row=6,column=3,sticky="w")

        self.output= tk.Text(root, height=20, width=65)
        self.output.grid(row=7,column=2,columnspan=4)

	
        self.frm_node = tk.Label(root)
        self.frm_node["text"]="    From"
        self.frm_node["fg"]="blue"
        self.frm_node.grid(row=3,column=2,sticky="es")

        self.to_node   = tk.Label(root)
        self.to_node["fg"]="blue"
        self.to_node["text"]="       To"
        self.to_node.grid(row=4,column=2,sticky="e")

        self.spacer = tk.Label(root)
        self.spacer ["text"]="    "
        self.spacer.grid(row=1,column=0)
        
        self.spacer2 = tk.Label(root)
        self.spacer2 ['text']="            "
        self.spacer2.grid(row=1,column=1)

        self.instruct = tk.Label(root)
        self.instruct ["text"]=" Highlight a node and then\n"+\
                "select FROM and TO \n then click Compute Path"
        self.instruct.grid(row=2,column=2,padx=20,columnspan=2)
        
        self.LabelList = tk.Label(root)
        self.LabelList["text"]="Node List: "
        self.LabelList.grid(row=2,column=1,sticky="s")
        
        self.avoidlabel=tk.Label(root)
        self.avoidlabel["text"]="      Avoid List:"
        self.avoidlabel.grid(row=3,column=4,columnspan=2,sticky="es")
        
        self.avoidit=tk.Listbox(root,width=12,height=5)
        self.avoidit.grid(row=4,column=4,columnspan=2,sticky="ne")
        
        global startchar
        startchar=tk.Entry(root,width=12)
        startchar.grid(row=4,column=1,columnspan=2,sticky="nw")                                               # ask them if they are sure
        startchar.bind("<Key>",checkkey) 
        startchar.focus_set() 
        
        frameb=tk.Frame(master=root,bg="blue",height=120,bd=2)
        frameb.grid(column=1,row=3)
        
        global listbox
        listbox=tk.Listbox(frameb,width=12,height=10)
        scrollbox = tk.Scrollbar(frameb, orient="vertical") 
        # Attach Scrollbar to Frame
        listbox.grid(row=3,column=1,rowspan=2,columnspan=2,sticky="w")
        scrollbox.grid(row=3,column=2,rowspan=2,sticky="ens")
        scrollbox.config( command = listbox.yview )
        listbox.configure(yscrollcommand=scrollbox.set)
        
        global graph
        for each in sorted(graph): # Populate listbox with list of nodes
            sellist.append(each)
            listbox.insert(tk.END,each) 
     
    def __init__(self, master):

        self.master=master
        tk.Frame.__init__(self, master,bg="red")
        self.grid(row=0,column=1)
        self.createWidgets()

        
def checkkey(event):    # Move to this letter in the listbox
        listbox.select_clear(0, 'end')  # Clear any existing selection
        global searchfor
        global startchar
        strlength=int(0)
        if event.keysym=="BackSpace":
            strlength=len(searchfor)-1
            searchfor=searchfor[0:strlength]
       
        else:
            if not event.char.isprintable :
                searchfor =" "
            else:
                addchar=event.char
                addchar=addchar.upper()
              #  print(addchar)
                searchfor=searchfor+addchar
        ix=0
        while sellist[ix] < searchfor and ix < len(sellist) -1 :
                ix =ix+1
        listbox.select_set(ix) # Select the first item starting with >
        listbox.yview(ix)      # Scroll the selection list to display
        startchar.delete(0,"end") # Delete prior from screen
        startchar.insert(0,searchfor)   # Put new search string contents
        return "break"  # Prevent tkinter from adding key to startchar
        
root = tk.Tk()
root.title(" Compute Mean Time Between Failure (MTBF) of a path")
root.geometry('700x700+0+0')

global startchar

f=open("graph.json","r")
gbuf=f.read()
f.close
graph=json.loads(gbuf) # Load list of nodes
sellist=[]
avoidlist=[]
searchfor=""
fromnode="not"
tonode="not"    # defaults that should never be used

app = Application(root)

root.protocol("WM_DELETE_WINDOW", app.callback) # If they X the window
                                        # ask them if they are sure

app.mainloop()

root.destroy()
