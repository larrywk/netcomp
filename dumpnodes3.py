
f=open("nodes.csv","r")
line=f.readline()
linecount=1
while line:
        aline=line.split("\n")
        sline=aline[0].split(",")
        print ("{:3d}".format(linecount),end="")
        print(" ",end="")
        print ("{:4}".format(sline[0]),end="")
        mtbf=int(sline[1])
        print (str("{0:,}".format(mtbf)).rjust(8))
        linecount = linecount + 1
        line =f.readline()

