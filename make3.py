# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
print("Processing it!")
fname = input("File to convert")
oldname=fname+".py"
f=open(oldname,"r")
buf=f.read()
newbuf=buf.replace("\t","    ")
f.close
f=open(fname+"3.py","w")
f.write(newbuf)
f.close()
print("Done")