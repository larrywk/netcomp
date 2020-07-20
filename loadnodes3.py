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

#nodelist=loadnodes({})


#print(nodelist)
#mtbf =nodelist.get("A")
#print mtbf

