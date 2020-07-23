# netcomp
Python code to compute best network path
If you load this code into a directory on a Linux machine with Python37 installed
you can then invoke it by running the go.sh script included

The input  files that you need are:
  1. nodes.csv, a comma seperatedvalues file with nodename, mean time between failure in hours
  2. spans.csv, a comma seperated values file with from node, to node, fiber path length, and a name for the shared risk link group
  
  at the command line run "python graphjson.py", which will create the file graph.json
  
