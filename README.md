# netcomp
This collection of Python code was written to demonstate how Python can be used to work on network engineering questions.
It contains modules that will read from comma seperated values files, and interact with the user via a GUI written with
the Python GUI toolkit tkinter.  The Python code has examples of most of the techniques you would need to build a custom 
app that would calculate things that network engineers have traditionally been doing by hand, with Excel, or something
like that.

It is a working example of computing the Mean Time Between Failure for a network path; finding the shortest path from any two points
in a list of spans, or taking a script with variables in it and doing the variable substitution.

Python code to compute best network path
If you load this code into a directory on a Linux machine with Python37 installed
you can then invoke it by running the go.sh script included.  Alternatively, it has been tested on Anaconda3 on Windows 10.

The input  files that you need are:
  1. nodes.csv, a comma seperatedvalues file with nodename, mean time between failure in hours
  2. spans.csv, a comma seperated values file with from node, to node, fiber path length, and a name for the shared risk link group
  
  at the command line run "python graphjson.py", which reads the spans.csv and will create the file graph.json
  
  It will create a results file in the current working directory, with a date-time stamp in the file name.
  
