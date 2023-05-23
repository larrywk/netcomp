# Python 3.7 by Larry Weeks
# Application to ask to pick from and to nodes from a list
# and then invoke a routine to find the shortest length path
# which is diverse from a shared risk link group list.
# 
import tkinter as tk
from tkinter import messagebox
import os
#from os import path
from datetime import datetime

def pathlen(path):  # Routine to calculate fiber path length

    totallength=0
    firsttime=0
    global spandict  # Dictionary of from comma to and index number
    global fiberlen  # Indexed list of fiber lengths
    global srlg      # shared risk link group
    global avoidlist # shared risk link groups to avoid for this path
   
    if not path:  # If the path you were passed does not exist
        return(totallength) # If no path, length=0, which means no path
    for each in path:  # for each node in the path
         if firsttime==0:
             lastnode=each # A span is a from to pair
             firsttime=1
             continue # no span until we have second node
         length=0
         if not firsttime == 0:
                fromto=lastnode+","+each  # current span
                ix=spandict[fromto]       # index number for this span
                length=float(fiberlen[ix]) # fiber length for this span
                
                spansrlg=srlg[ix] # shared risk link group for this span
         if spansrlg in avoidlist:
          #  print("Avoiding",spansrlg)
            return(0) # This path has an avoid
         totallength=totallength+length
         lastnode=each
     

    return(totallength)


def spanlookup():  # Routine to read comma seperated values
    f =  open("spans.csv","r")  # And load them into global arrays
    wholething=f.read()
    byline=wholething.split("\n")
    lineix = 0
    global graph   #  dictionary of nodes and their neighbors
    global spandict # spans and their index value
    global fiberlen  # fiber length indexed by span
    global srlg      # shared risk link group identifier for span
    #startat="zero"
    #srlg.append(startat)  # start counting at 1
    #fiberlen.append(0)    #
    for line in byline:

        if len(line.split(",")) < 2:    # if less than two commas
             continue                 # presume last line of file
        
        node,dest,fiberlength,spansrlg=line.split(",")
        fromto=node+","+dest    # from-node comma to-node
        spandict.update({fromto:lineix})
        fiberlen.append(fiberlength)
        srlg.append(spansrlg)
        
        #
                 
        if not node in graph : # First time we saw this node
            destnode=[dest]
            newnode={node:destnode}
            graph.update(newnode)
            existing=[]
        else:
            existing=graph[node] # Existing list of destination nodes
            if dest in existing:
                 tk.messagebox.showwarning \
                 ("warning", dest+"already in "+node)
            existing.append(dest)
            newnode={node:existing}
            graph.update(newnode)
            # End of for loop
        lineix=lineix+1
    return()   # end of spans.csv


         
    
def find_shortest_path(graph, start, end, path=[]):
       # recursive walk of graph to find paths       
       
        path = path + [start]  # add current node to the end of the path
        if start == end:       # if path has reached destination
            return path        # return it as the answer
        if not start in graph:  # if there is no such node
            return None
        shortest = None         # Haven't found it so far
        for node in graph[start]:  # for each link from where we are
            if node not in path:    # and we haven't been there already
                newpath = find_shortest_path(graph, node, end, path)
                newlen=pathlen(newpath)
                shortlen=0
                if shortest: # set in prior iteration of for loop
                    shortlen=pathlen(shortest)
                if newpath and newlen > 0 :  # newlen=0 = hit avoid list
                    #if not shortest or len(newpath) < len(shortest):
                   if not shortest or newlen < shortlen:
                        shortest = newpath
        return shortest
    
def runshortest(startnode,endnode,fname):
   
    global fo  #  Output file handle
    global fiberlen   # Array of spans fiber length
    global srlg       # span belongs to a shared risk link group
    global avoidlist  # list of srlgs to avoid
    global spandict   # dictionary of spans and their index
    global srlglist  # List of shared risk link groups in this path
    
    
    fo=open(fname,"w") # Open output file
   
    
    srlglist=[]    # clear list of srlgs on this path
    if avoidlist:  # If there is an avoid list
       pavoidlist=str(avoidlist)  # Only strings can write
       fo.write ( "Avoiding ")   # put avoid
       fo.write(pavoidlist)
       fo.write("\n")
       
    global avoidit  # Listbox widget  
    avoidit.delete(0,tk.END)  # Clear prvious contents
    
    fo.write("Results in:")  # Put name of output file in display
    fo.write(fname)
    fo.write("\n")
    
    result=find_shortest_path(graph,startnode,endnode)
    
    fo.write("Looking for ")
    fo.write(startnode)
    fo.write(" to ")
    fo.write(endnode)
    fo.write("\n")
    
    presult=str(result)
    fo.write(presult)   # List of node names of best path
    fo.write("\n")
    
    firsttime=0
    if result:  # if result is not None, i.e. we found a path
        fromnode=startnode
  
        totallength=0
        
        avoidit.delete(0,tk.END)  # Clear existing srlg list to avoid
        #print(srlg)
        fo.write( "             Span       Total")
        fo.write("\n")
        fo.write ("Node         Length     Length  SRLG \n")

        for each in result:
            a= ('{:8}'.format(each))
            fo.write (a)	#  add per node processing here
  
            if not firsttime == 0:
                fromto=fromnode+","+each
                ix=spandict[fromto]
                length=fiberlen[ix]
                spansrlg=srlg[ix]
               
            
            if not firsttime == 0:
                fo.write ('{:,}'.format(int(length)).rjust(11))
                totallength=totallength+int(length)
                fo.write ('{:,}'.format(totallength).rjust(11))
                fo.write("  ")
                fo.write(spansrlg)
                fo.write(" ")
                fo.write(str(ix))
                
                if spansrlg not in srlglist:# New list for next time
                    srlglist.append(spansrlg)
                  
                fromnode=each
            fo.write ("\n")
            firsttime=1
            
    avoidlist=srlglist
    avoidlist.sort()
   # print(avoidlist)
    last=""
    for each in avoidlist:
        if each != last:  # Add only unique values
            avoidit.insert(tk.END,each)
            last=each
    avoidit.grid()  # repaint screen
    
    fo.close()   # Close output results file
   

class Application(tk.Frame):
    def callback(ignore):
        if tk.messagebox.askokcancel("Quit", \
                                      "Do you really wish to quit?"):
             root.destroy()
             os.sys.exit()

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
        fname=open("srlglist.csv","w")
        fname.close() # Empty the avoid node comma seperated values file
        self.clear_avoid.grid_remove() # Remove the button for clearing
        avoidit.delete(0,"end") # Delete prior from screen
        global avoidlist
        avoidlist=[]   # Zero out the list
        
    def add_avoid(self):
        global SRLG_Box
        global avoidlist
        global avoidit
        selval=SRLG_Box.curselection()
        if selval:  # Ignoore button click if nothing selected
        
            value=SRLG_Box.get(SRLG_Box.curselection())
            avoidit.insert(tk.END,value)
            avoidlist.append(value)
            avoidit.grid()  # Repaint screen

            self.clear_avoid.grid(row=5,column=5,sticky="e") # Redisplay

    def compute_pth(self):
        global timestampStr
        if fromnode == "not" or tonode == "not":
            tk.messagebox.showwarning\
                ("Warning","Please select from and to nodes")
            return()
    #
        
     
        fname="result-"+timestampStr
    
   #     if os.path.exists(fname):
    #        tk.messagebox.showwarning("Warning", fname+" already exists")
     

        # runs routine to find best path between nodes
        runshortest(fromnode, tonode,fname)
	     
        f=open(fname,"r")  # fname = results output file
        buf=f.read()
        f.close()
        
        self.output.delete("1.0","end") # Delete prior from screen
        self.output.insert("1.0",buf)   # Put new output file contents
	                                    # On the screen
        self.clear_avoid.grid(row=5,column=5) # Redisplay if it was hidden
 
            

    def createWidgets(self):   # Build the tkinter widgets
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
        self.sel_to_node.grid(row=4,column=3,sticky="wn")
        
        self.addavoid = tk.Button(root)
        self.addavoid["text"]="Add AVOID SRLG"
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

        self.output= tk.Text(root, height=15, width=65)
        self.output.grid(row=7,column=2,columnspan=4)

	
        self.frm_node = tk.Label(root)
        self.frm_node["text"]="    From"
        self.frm_node["fg"]="blue"
        self.frm_node.grid(row=3,column=2,sticky="es")

        self.to_node   = tk.Label(root)
        self.to_node["fg"]="blue"
        self.to_node["text"]="       To"
        self.to_node.grid(row=4,column=2,sticky="en")

        self.spacer0 = tk.Label(root)
        self.spacer0 ["text"]="    "
        self.spacer0.grid(row=1,column=0)
        
        self.spacer1 = tk.Label(root)
        self.spacer1 ['text']="        "
        self.spacer1.grid(row=1,column=1)

        self.spacer2 = tk.Label(root)
        self.spacer2["text"]="            "
        
        self.instruct = tk.Label(root,width=28)
        self.instruct ["text"]=" Highlight a node and then\n"+\
                "select FROM and TO \n then click Compute Path"
        self.instruct.grid(row=2,column=3,padx=20,columnspan=2)
        
        self.LabelList = tk.Label(root)
        self.LabelList["text"]="Node List:   SRLG List:"
        self.LabelList.grid(row=2,column=1,sticky="sw")
       
        
        self.avoidlabel=tk.Label(root)
        self.avoidlabel["text"]="      Avoid List:"
        self.avoidlabel.grid(row=3,column=4,columnspan=2,sticky="es")
        
        global avoidit
        avoidit=tk.Listbox(root,width=12,height=5)
        avoidit.grid(row=4,column=4,columnspan=2,sticky="ne")
        
        for each in avoidlist:
            avoidit.insert(tk.END,each)  # initial values loaded from file
        f.close()
        
        self.startchar=tk.Text(root,height=1,width=12)
        self.startchar.grid(row=4,column=1,columnspan=2,sticky="nw")                                               # ask them if they are sure
        self.startchar.bind("<Key>",checkkey) # runs checkkey on keypress
        self.startchar.focus_set() 
        
        frameb=tk.Frame(master=root,bg="blue",height=120,bd=2)
        frameb.grid(column=1,row=3) # scrollbars need to be in a frame
                                    # with the listbox they go to
        
        global listbox  # global so we can reference it elsewhere
        listbox=tk.Listbox(frameb,width=12,height=10)
        scrollbox = tk.Scrollbar(frameb, orient="vertical") 
        # Attach Scrollbar to Frame
        listbox.grid(row=3,column=1,rowspan=2,columnspan=2,sticky="w")
        scrollbox.grid(row=3,column=2,rowspan=2,sticky="ens")
        scrollbox.config( command = listbox.yview )
        listbox.configure(yscrollcommand=scrollbox.set)
        
        global SRLG_Box
        SRLG_Box=tk.Listbox(frameb,width=12,height=8)
        SRLG_scroll=tk.Scrollbar(frameb,orient="vertical")
        SRLG_Box.grid(row=3,column=4)
        SRLG_scroll.grid(row=3,column=4,sticky="ens")
        SRLG_Box.configure(yscrollcommand=SRLG_scroll.set) 
        SRLG_scroll.config(command=SRLG_Box.yview)
        
        last=""
        #print(srlg)
        for each in srlg:    sortedsrlg.append(each)		 # need to preserve the index order of srlg
        sortedsrlg.sort()  # but need to process in order to remove dups
        for each in sortedsrlg:
            if each != last :  # We just load unique values in order
                SRLG_Box.insert(tk.END,each)  # in the listbox
            last=each
        f.close()
        
        global graph
        for each in sorted(graph): # Populate listbox with list of nodes
            sellist.append(each)   # selection list that corresponds to
            listbox.insert(tk.END,each)  # listbox
     
    def __init__(self, master):  # Black magic borrowed from example
                                 # on the Internet
        self.master=master     # _init_ is called at invocation of the class
        tk.Frame.__init__(self, master,bg="red") # Initializes root window
        self.grid(row=0,column=1)
        self.createWidgets()

        
def checkkey(event):    # Move to this letter in the listbox
        listbox.select_clear(0, 'end')  # Clear any existing selection
        global searchfor
        strlength=int(0)
        if event.keysym=="BackSpace":
            strlength=len(searchfor)-1
            searchfor=searchfor[0:strlength] # backspace remove last char
       #
            
        else:
            if not event.char.isprintable : # any non printable zeros search
                searchfor =" "
  
            else: searchfor=searchfor+event.char
       
        ix=0  # Lookthrough the list for last item <= search string
        while sellist[ix] < searchfor and ix < len(sellist) -1 :
                ix =ix+1
        listbox.select_set(ix) # Select the first item starting with >
        listbox.yview(ix)      # Scroll the selection list to display
        
 #--------   Start of main code ----------------------------
global fiberlen
global srlg
global sortedsrlg
global spandict
global avoidlist  #  list of srlgs to be avoided
global graph
global timestampStr  # time program was invoked


fiberlen=[]  # List of fiber span lengths
srlg=[]      # List of shared risk link groups 
sortedsrlg=[] 
sellist=[]   # selection list with contents of listbox
avoidlist=[] # list of srlg's to avoid
spandict={}  # dictionary of spans and their index number
graph={}     # dictionary of nodes and their neighbors
searchfor=""
fromnode="not"
tonode=  "not"    # defaults that should never be used
   
dateTimeObj = datetime.now()

timestampStr = dateTimeObj.strftime("%Y-%m-%d-%H-%M-%S") 

spanlookup()   # Loads fiberlen and srlg lists, builds graph


f = open("srlglist.csv","r")   # load shared risk link group
                               #  from prior run
byline = f.read().split("\n")
f.close()
for line in byline:
    if line > " ":
        avoidlist.append(line)  # builds list of srlgs to avoid
            
            
root = tk.Tk()
blank_space=" "
root.title(".                                 Compute Shortest path which avoids SRLGs")
root.geometry('1000x700+50+50')

app = Application(root)  # instantiate class

root.protocol("WM_DELETE_WINDOW", app.callback) # If they X the window
                                        # ask them if they are sure

app.mainloop()   # Turns control over to screen

root.destroy()  # Delete all the window stuff
