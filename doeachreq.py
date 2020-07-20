#Python 3 Larry Weeks
#Read a list of requirement
import calcshortest

fname=open("reqs.csv","r")
wholebuf=fname.read()
lines=wholebuf.split("\n")
for line in lines:
    if len(line.split(",")) < 3 : break
    reqnum,speed,fromnode,tonode=line.split(",")
    print("Requirement=",reqnum)

    calcshortest.calcshortest(reqnum,speed,fromnode,tonode)
fname.close()

