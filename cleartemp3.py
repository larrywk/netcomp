import glob
import os
list =glob.glob("/home/larry/work/*.pyc")
list.sort()
for each in list:
    print (each)
answer = input("Delete?").upper()
if  answer == "YES":
    for each in list:
        os.remove(each)
    print ("Removed")
print ("Done")
