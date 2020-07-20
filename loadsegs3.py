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
         
    

#graph=loadsegs({})

#print(graph)

