# netcomp
This collection of Python code was written to demonstate how Python can be used to work on network engineering questions.
It contains modules that will read from comma seperated values files, and interact with the user via a GUI written with
the Python GUI toolkit tkinter.  The Python code has examples of most of the techniques you would need to build a custom 
app that would calculate things that network engineers have traditionally been doing by hand, with Excel, or something
like that.

It contains a working example of finding the shortest path from any two points
in a list of spans, or taking a script with variables in it and doing the variable substitution.


If you load this code into a directory on a Linux machine with Python37 and python3-tk (tkinter) installed and with X11 capabilities,
you can then invoke it by running the go.sh script included.  Alternatively, it has been tested on Anaconda3 on Windows 10.

The input  file that you need is maintained by table_manager.py
  
When you run the diverse path computation, it will give you an option to create a results file in the current working directory, with a date-time stamp in the file name.
  
