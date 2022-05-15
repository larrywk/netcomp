# netcomp
This collection of Python code was written to demonstate how Python can be used to work on network engineering questions.
It contains modules that will read from comma seperated values files, and interact with the user via a GUI written with
the Python GUI toolkit tkinter.  The Python code has examples of most of the techniques you would need to build a custom 
app that would calculate things that network engineers have traditionally been doing by hand, with Excel, or something
like that.

It contains a working example of computing the Mean Time Between Failure for a network path; finding the shortest path from any two points
in a list of spans, or taking a script with variables in it and doing the variable substitution.


If you load this code into a directory on a Linux machine with Python37 and python3-tk (tkinter) installed and with X11 capabilities,
you can then invoke it by running the go.sh script included.  Alternatively, it has been tested on Anaconda3 on Windows 10.

The input  files that you need are:
  1. nodes.csv, a comma seperated values file with two fields, nodename, which is just a text label for a network node,
     and the mean time between failure rating in hours
  2. spans.csv, a comma seperated values file with from node, to node, fiber path length, and a name for the shared risk link group,
  
  If the spans.csv file is changed, then 
  at the command line run "python graphjson.py", which reads the spans.csv and will create the file graph.json.
  
  When you run the diverse path computation, it will create a results file in the current working directory, with a date-time stamp in the file name.
  
