import pickle

def graphdump(graph):
    #dumpfile=open("graph.txt","w")
    for each in sorted( graph):
        result=graph[each]
    #    dumpfile.write(each.rjust(8))
#	dumpfile.write(":")
#	dumpfile.write(str(result) )
#       dumpfile.write("\n")
        line=each+":"
        
        line=line.rjust(8)
                               
        
        print (line,end="")
        for node in result:
            print (node,end="")
            print(" ",end="")
        print ("")
        #print "------"
#    dumpfile.close()

 
graph=pickle.load(open("graph.pkl","rb"))
graphdump(graph)
