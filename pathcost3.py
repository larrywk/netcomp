#Python 3.7 Larry Weeks
def pathcost(path,nodelist):

    totalmtbf=0
    if not path:
        return(totalmtbf) # If no path, MTBF=0
    for each in path:
      
        temp=nodelist.get(each)
        mtbf=0
        if temp:
            mtbf=float(temp[0])

        if totalmtbf == 0 :
            totalmtbf=mtbf
        else:
            if temp: totalmtbf = (totalmtbf*mtbf)/(totalmtbf+mtbf)
            
    return(totalmtbf)
