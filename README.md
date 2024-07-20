BunPy is a stripped-down Python version of BunVis, a program used in the Mauk lab for decades to analyze eyelid conditioning data and to make figures from such data. 
The current version only works for virtual eyelid responses from our cerebellar simulation. 
Adding the ability to analyze real eyelid data collected with the current and old version of BunTrain are ongoing. 
That version will automatically detect the version from the data files and adjust accordingly.
BunPy can do two basic things: 
  display a waterfall plot of eyelid responses and output in csv format
  numerical analysis of the eyelid responses. 
BunPy imports and eyelidX.py file, where most of the work is done.
BunPyX.py has only a few lines to make it easier to navigate the things that can be controlled within it. 

Two data files are required. 
  A .dat file, which contains the eyelid traces in binary format
  a .bvi file, which is a text file with details about the session and about the trials that BunPy needs for the analyses. 

To run BunPy you need both the BunPy.py file and the Eyelid.py file (current versions are BunPy02.py and eyelid02.py) saved in the same folder, as well as the .dat and .bvi files to be analyzed.
Future versions may add file navigating features, but for now line 3 of the program is where you specify the .dat file, which must be in the same directory. BunPy will automatically find the .bvi file of the same name.

Things you can control:
Line 3)  The name of the .dat file
Line 4) 	The name of the output file for numeric data (the .csv suffix will be added). This is ignored if numerical analyses are not selected.
Line 6) Select the tasks desired: 0 = waterfall only, 1 = numeric only, 2 = both
Line 7) Indicate the number of points to be drawn for each sweep in waterfall plot. For all current data files sweeps are 2500 points, each 1 msec, where the CS onset is at point 201. Setting drawto = 0 draws all points. These numbers assume that the first trial is number 1.
Lines 7 and 8) Select the first and last trials for the waterfall plot. Many of our simulation data files have too many trials to display in a single waterfall. Set end file to 0 to draw all trials. 

A few pro tips: 
  To use a waterfall plot in a figure make a screen shot of the waterfall window (left alt – shift – printscreen for windows) and paste it into the target program (PowerPoint, Adobe Illustrator, etc.)
  The format of the csv file containing numeric data is in the same format outputted by BunVis. Because of this, there are many excel templates floating around that automat almost all analyses you would typically want to do. I will soon load one into GitHub.
