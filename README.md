# BiologicalMotionExperiment
### *Project: Biological motion for visual cortex induced phosphenes*

The map Figure_Generation_MATLAB contains the codes  	`DotFigureGenerator.m` and	`StickfigureGenerator.m` for the generation of videos of containing biological motion walker with various frame duration and a certain limited lifetime. This code requires you to download Psychtoolbox and Biomotion toolbox. Also the positions of the walkers can be changed by adjusting the coordinates (explained oin the file). 

For running the experiment for subjects, use the code in src:
<br>
Lynn_BiMoExp_fun is a file that can be used in two ways:
  1. Run the file to start the experiment 
  2. Import the file into another python code to use the class methods 
    <br> (`from Lynn_BiMoExp_fun import Running_experiment`). An example run code is included in the src map, to show how you can import and use the file.


When running the file, you must have the maps in the same directory: 
<br>
  - introduction: contains all the images with text that are shown during the experiment.

  - experiment: The four experiments, Dotfigure_LLQ, Dotfigure_center, Phosphenefigure_LLQ, Phosphenefigure_center.

  - experiment data: the csv data file that is outputted from the experiment is automatically saved in this map. 
<br>
It is important that the maps are organized in this way, for the code to work.
<br>
OpenCV needs to be downloaded to run the program ( `pip install cv2` ). 



