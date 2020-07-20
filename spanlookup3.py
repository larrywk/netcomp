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
#
#fiberlen=[]

#spandict=spanlookup({})

#print(spandict)
#fromto="FA"
#while fromto > "A":
#    fromto=raw_input("Span?")
    #if fromto in spandict:
    #    print spandict[fromto],
    #    print fiberlen[spandict[fromto]]

