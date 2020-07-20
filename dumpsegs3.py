#Python 3.7 Larry Weeks  Format csv for printing
f=open("spans.csv","r")
line=f.readline()
linecount=1
while line:
        aline=line.split("\n")[0]
        print ("{:4d}".format(linecount),end="",sep=" ")
        print (" ",end="")
        bline=aline.split(",")
        fromnode = bline[0]
        tonode = bline[1]
        fiberlen=int(bline[2])
        srlgname=bline[3]
        linecount = linecount + 1
        print ("{:8}".format(fromnode),end="")
        print ("{:8}".format(tonode),end="")
        print( "{:8,}".format(fiberlen).rjust(6),"  ",end="")
        if srlgname: print("{:8}".format(srlgname))
        line =f.readline()

