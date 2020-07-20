import calcbkup

fname=open("reqsbkup.csv","r")
wholebuf=fname.read()
lines=wholebuf.split("\n")
for line in lines:
    if len(line.split(",")) < 3 : break
    reqnum,speed,fromnode,tonode=line.split(",")

    calcbkup.calcbkup(reqnum,speed,fromnode,tonode)
fname.close()

