import loadsegs3
import pickle

def graphdump(graph):
    dumpfile=open("graph.txt","w")
    for each in sorted(graph):
        result=graph[each]
        dumpfile.write(each.rjust(8))
        dumpfile.write(":")
        dumpfile.write(str(result) )
        dumpfile.write("\n")
        print (each.rjust(8),":",result)
        #print "------"
    dumpfile.close()

 
graph=loadsegs3.loadsegs({})
graphdump(graph)

pickle.dump(graph,open("graph.pkl","wb"))

