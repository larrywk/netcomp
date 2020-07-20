#import sys
# insert at 1, 0 is the script path (or '' in REPL)
#sys.path.insert(1, '/home/larry/src')
def calcshortest(reqnum,speed,nodefrom,nodeto):
    import loadsegs3         # load fiber spans
    import findshortest3     # find shortest path 
 #   import loadnodes        # Load nodes MTBF
  #  import spanlookup       # Load span lengths table

   # fiberlen=[]             # List of fiber span lengths

    graph=loadsegs3.loadsegs({})
  #  spandict=spanlookup.spanlookup({},fiberlen)
   # nodelist=loadnodes.loadnodes({})
    startnode=nodefrom
    endnode=nodeto
   
    result=findshortest3.find_shortest_path(graph,startnode,endnode)
#print nodelist
    print(result)   # List of node names of best path
    if result:
        resultsfile=open("../results/nodereqs.csv","a")
        ix = 0
        for each in result:
            if ix > 0 : prior=result[ix-1]
            if each == nodefrom : prior="start"
            if len(result) > ix+1 :  nextnode=result[ix+1]
            if each == nodeto: nextnode="end"
            line=reqnum+','+speed+','+prior+","+each+','+nextnode+"\n"
            resultsfile.write(line)
            ix = ix +1
        resultsfile.close()
