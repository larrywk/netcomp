# Python 3.7 by Larry Weeks
import sys
#import loadsegs3         # load fiber spans
#import findshortest3     # find shortest path 
#import loadnodes3       # Load nodes MTBF
#import spanlookup3       # Load span lengths tabl
from datetime import datetime

def loadnodes(nodelist):

    f =  open("nodes.csv","r")
    wholething=f.read()
    byline=wholething.split("\n")
    nodecount=0
    for line in byline:
        if len(line.split(",")) < 2:
           break # end of file
		#print(line)
        node,mtbf=line.split(",")
        if not node in nodelist:
            nodemtbf=[mtbf]
            newnode={node:nodemtbf}
            nodelist.update(newnode)
            nodecount=nodecount+1
        else:
        		print ("Duplicate node",node)
   # print ("Nodes loaded=",nodecount)
   # a=input("Ending loadnodes")
    return(nodelist)


def find_shortest_path(graph, start, end, path=[]):
        nodelist=loadnodes({})
       
        path = path + [start]  # add current node to the end of the path
        if start == end:       # if path has reached destination
            return path        # return it as the answer
        if not start in graph:  # if there is no such node
            return None
        shortest = None
        for node in graph[start]:  # for each link from where we are
            if node not in path:    # and we haven't been there already
                newpath = find_shortest_path(graph, node, end, path)
                newcost=pathcost(newpath,nodelist)
                shortcost=0
                if shortest:
                    shortcost=pathcost(shortest,nodelist)
                if newpath:
                    #if not shortest or len(newpath) < len(shortest):
                   if not shortest or newcost > shortcost:
                        shortest = newpath
      
        return shortest


def pathcost(path,nodelist):

    totalmtbf=0
    if not path:
        return(totalmtbf) # If no path, MTBF=0
    for each in path:
      
        temp=nodelist.get(each)
        mtbf=0
        if temp:
            mtbf=float(temp[0])

        if totalmtbf == 0 :
            totalmtbf=mtbf
        else:
            if temp: totalmtbf = (totalmtbf*mtbf)/(totalmtbf+mtbf)
            
    return(totalmtbf)


def loadsegs(graph):
    f = open("avoid.csv","r")
    avoidlist=[]
    byline = f.read().split("\n")
    for line in byline:
        if line > " ":
            avoidlist.append(line)
    if avoidlist:
        print ( "Avoiding",avoidlist)
    f =  open("spans.csv","r")
    wholething=f.read()
    byline=wholething.split("\n")
    
    for line in byline:
         a=line.split(",")
        
         if len(a) < 2:
	         break
		#print(line)
            
         node,dest,fiberlen,srlg=line.split(",")
        #
      
         if dest not  in \
            avoidlist :
               # print(""),
            
            if not node in graph :
               destnode=[dest]
               newnode={node:destnode}
               graph.update(newnode)
               existing=[]
            else:
                existing=graph[node]
            if dest in existing:
                 print (dest,"already in ",node)
            existing.append(dest)
            newnode={node:existing}
            graph.update(newnode)
            # End of for loop
    return(graph)

def spanlookup(spandict,fiberlen,srlg):
    f =  open("spans.csv","r")
    wholething=f.read()
    byline=wholething.split("\n")
    lineix = 0
    for line in byline:

        if len(line.split(",")) < 2:    # if less than two commas
             break                  # presume last line of file
        #print(line)
        aline=line.split(",")
        fromto=aline[0]+","+aline[1]    # from-node comma to-node
        spandict.update({fromto:lineix})
#        print len(line.split(","))
        fiberlen.append(line.split(",")[2])
        srlg.append(line.split(",")[3])
        lineix=lineix+1
    return(spandict)



dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%Y-%m-%d-%H:%M:%S")

print("Run "+timestampStr)
print("")


fiberlen=[] # List of fiber span lengths
srlg=[]     # List of shared risk link groups

graph=loadsegs({})
spandict=spanlookup({},fiberlen,srlg)
nodelist=loadnodes({})
if len(sys.argv) > 1:  # Presume we were called by asknodes.py
    startnode = sys.argv[1].upper()
    endnode =  sys.argv[2].upper()
else:
    startnode=input("Startnode?")  # Run from command line
    endnode=input("Endnode?")


result=find_shortest_path(graph,startnode,endnode)

print(result)   # List of node names of best path
firsttime=0
if result:
    fromnode=startnode
    totalmtbf=0
    totallength=0
    srlglist=[]  # List of shared risk link groups in this path
    print( "             Node     Total      Span       Total")
    print ("Node         MTBF     MTBF       Length     Length  SRLG")

    for each in result:
        a= ('{:8}'.format(each))
        print (a,end="")	#  add per node processing here
  
             #   print nodelist
        if not each in nodelist:  # Fiber span no MTBF
            temp = None
            print ( "                    ",end="")  # leave MTBF blank
        else:
            temp=nodelist.get(each)
        if not firsttime == 0:
            fromto=fromnode+","+each
              
            ix=spandict[fromto]
            length=fiberlen[ix]
            spansrlg=srlg[ix]
        if temp:
            mtbf=float(temp[0])
            a=str('{0:,.0f}'.format(mtbf)).rjust(9)
            print(a,end="")
            #p=p.rjust(10)
            #print p,
            if totalmtbf == 0 :
                totalmtbf=mtbf
            else:
                totalmtbf = (totalmtbf*mtbf)/(totalmtbf+mtbf)
            print ('{:,.02f}'.format(totalmtbf).rjust(11),end="")
        if not firsttime == 0:
            print ('{:,}'.format(int(length)).rjust(11),end="")
            totallength=totallength+int(length)
            print ('{:,}'.format(totallength).rjust(11),end="")
            print("  ",spansrlg,end="")
            if spansrlg not in srlglist:
                srlglist.append(spansrlg)
        firsttime=1
        fromnode=each
        print ("")
            
    firsttime=0
    f=open("avoid.csv","w")
    result.pop()      # remove last node
    for each in result:
        if not firsttime == 0:
            line=each+"\n"
            f.write(line)
        firsttime = 1
    f.close
    
    srlglist.sort()
    
    f=open("srlglist.csv","w")
    for  each in srlglist:
        line=each+"\n"
        f.write(line)
    f.close() 
    print ("Done")
