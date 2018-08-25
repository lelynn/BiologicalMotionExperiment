
# coding: utf-8

# # Lynn Le 2018

# # Experimental set-up for different frame durations

# ### **Imported libraries: **


# In[1]:


import cv2
import numpy as np
import time
import os
import pandas as pd
from sklearn.utils import shuffle
import sys

import matplotlib
import matplotlib.pyplot as plt
from pandas.plotting import *


# ### **These are the simulation videos :**
# 

# In[3]:


#These are the simulation videos that are put into a dataframe (videos_df). There are a total of 20 unique videos and will eventually be shuffled the order and multiplied 5 times. 
run_directory = '/Users/lynn/Desktop/EXPERIMENT DIRECTORY/BioMotion Phosphene Experiments'
videos_df = pd.DataFrame(columns=['filename','fwd/bckwd', 'm/o', 'frame duration in ms'])
experiment = '/experiment/' +'OriginalExperiment/' #'CENdots+pgExperiment/', 'LLQDotsExperiment/', OriginalExperiment,'LLQLines+pgExperiment/'

video_path = run_directory + experiment + 'FinalVideos/'

videos_df = pd.DataFrame(columns=['filename','fwd/bckwd', 'm/o', 'frame duration in ms'])
    
for v in os.listdir(video_path+'Forward/Original'):
    if v.endswith('.mp4'):
        videos_df =videos_df.append({'filename':'Forward/Original/'+v,'fwd/bckwd': "Forward", 'm/o': "o", 'frame duration in ms': v[7:v.find('[')]},ignore_index=True)

for v in os.listdir(video_path+'Forward/Mirror'):
    if v.endswith('.mp4'):
        videos_df =videos_df.append({'filename':'Forward/Mirror/'+v,'fwd/bckwd': "Forward", 'm/o': "m", 'frame duration in ms': v[9:v.find('[')]},ignore_index=True)

for v in os.listdir(video_path+'Reverse/Mirror'):
    if v.endswith('.mp4'):
        videos_df =videos_df.append({'filename':'Reverse/Mirror/'+v,'fwd/bckwd': "Backward", 'm/o': "o", 'frame duration in ms': v[9:v.find('[')]},ignore_index=True)

for v in os.listdir(video_path+'Reverse/Original'):
    if v.endswith('.mp4'):
        videos_df =videos_df.append({'filename':'Reverse/Original/' +v ,'fwd/bckwd': "Backward", 'm/o': "m", 'frame duration in ms': v[7:v.find('[')]},ignore_index=True)

videos_df


# ### ** A function to play demo videos:**
# 

# In[4]:


path_to_demovid = run_directory + experiment + 'Demo Videos/'
def play_two_demovids(demovid_filename1):
   # cv2.destroyAllWindows()
    cap = cv2.VideoCapture(path_to_demovid + demovid_filename1 )
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    else:
        framerate = cap.get(5)
    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True: 
            make_fixationpoint(frame)
            capname = "cap"
            #allows the resizing and centering of the video window
            cv2.namedWindow(capname, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(capname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow(capname, frame)
            cv2.waitKeyEx(40)
        else: 
            break


# ### ** A funtion to show images:**

# In[5]:


path_to_img =  run_directory + '/Introduction/Images/'
def show_image(image_filename):
    ''' Function shows image'''
    img = cv2.imread(path_to_img + image_filename)
    line2 = make_fixationpoint(img)
    winname = "cap"
    cv2.namedWindow(winname, cv2.WND_PROP_FULLSCREEN)          
    cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(winname,line2)


# #### ** A function to make fixationpoint** 

# In[6]:


def make_fixationpoint(img):
    ''' This function creates a fixation point for the center of the screen, param img refers to frame'''
    img_height = int(img.shape[0]/2)
    img_width = int(img.shape[1]/2)

    line1 = cv2.line(img,
    (img_width,img_height-5),
    (img_width,img_height+5),
    #color
    (0, 0, 255),
    #linethickness
    1)

    line2 = cv2.line(
    line1,
    (img_width-5,img_height),
    (img_width+5,img_height),
    #color
    (0, 0, 255),
    1)
    return line2


# ### ** A recursion to check keys and force key press.**

# In[8]:



def checks_which_key(image_filename, which_keys, wait_key_ms = 0):
    show_image(image_filename)
    which_key_check = cv2.waitKeyEx(wait_key_ms)
    if which_key_check in which_keys:
        return which_key_check
    else:
        show_image('try_again.png')
        cv2.waitKey(500)
        return checks_which_key(image_filename, which_keys)
    


# ### **TrialRun to practice**

# In[9]:


shuffled_test_samples = shuffle(videos_df.head(10)
                          )
def run_test():
    for i, sample in shuffled_test_samples.iterrows():
    
        shuffled_filename = sample['filename']

        cap = cv2.VideoCapture(video_path + shuffled_filename)

        if (cap.isOpened()== False): 
            print("Error opening video stream or file")
        else:
            framerate = cap.get(5)
            #vid_width = int(cap.get(3)/2)
            #vid_height = int(cap.get(4)/2)

        # Read until video is completed
        line2 = make_fixationpoint(np.zeros((600,800,3))) 
        cv2.imshow('cap', line2)
        cv2.waitKeyEx(500)
        while(cap.isOpened()):
          # Capture frame-by-frame
            ret, frame = cap.read()       
            if ret == True:
                capname = "cap"

                line2 = make_fixationpoint(frame)

                #Display the resulting frame
                cv2.namedWindow(capname, cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty(capname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                #cv2.imshow(capname, frame)
                cv2.imshow(capname, line2)

                if cv2.waitKeyEx(int(1000/framerate)) != -1:
                    time.sleep(1/framerate)  
          # Break the loop
            else: 
                break             
        cap.release()
        k = -1
        if k != Forwardkey and k != Backwardkey:
            k = checks_which_key('blank_image.png', [Forwardkey, Backwardkey])
    


# ### ** The code for displaying experimental set-up:**

# In[ ]:


#Enter subject name here:
subjectname = 'Testing123445'
#Configuration
#Determining the 'forward' Key by pressing a key

datapath =  run_directory + '/experiment data/'
data_filename = datapath+subjectname+'.csv'

columns_df = pd.DataFrame(columns=["filename", 
                                  "fwd/bckwd", 
                                  "m/o", 
                                  "frame duration in ms", 
                                  "answer", 
                                  "time"])
columns_df.to_csv(data_filename, mode='a')



show_image('indicate_forward.png')
Forwardkey = cv2.waitKeyEx(0)

#Determining the 'backward' Key
show_image('indicate_backward.png')
Backwardkey = cv2.waitKeyEx(0)

#Determining the 'continue' Key
show_image('indicate_continue.png')
Continuekey = cv2.waitKeyEx(0)

#show what is forward

show_image('Forward_before.png')
cv2.waitKeyEx(0)
play_two_demovids('FwdMirror60demo.mp4')
play_two_demovids('FwdOrig60demo.mp4') 

#FORWARD DEMOVID
#check_forward_press

  
checks_which_key('Forward_after.png', [Forwardkey])
show_image('well_done.png')
cv2.waitKey(500)        
#show what is backward

show_image('Backward_before.png')
cv2.waitKeyEx(0)


play_two_demovids('RevMirror60demo.mp4')
play_two_demovids('RevOrig60demo.mp4')

checks_which_key('Backward_after.png', [Backwardkey])
show_image('well_done.png')
cv2.waitKey(500)

#show what is forward
show_image('Your_task.png')
cv2.waitKeyEx(0)    

#print 'Forward = ', Forwardkey
#print 'Backward = ', Backwardkey
run_test()

shuffled_samples = shuffle(videos_df
                          )
pausecounter = 50

for i, sample in shuffled_samples.iterrows():
    
    if pausecounter == 0:
        
        checks_which_key('continue.png', [Continuekey], 120000)
       # while cv2.waitKeyEx(120000) != Continuekey: #break 2 minutes
            #show_image('continue.png')
        pausecounter = 50
    else:
        pausecounter -= 1
    
    shuffled_filename = sample['filename']
    
    cap = cv2.VideoCapture(video_path + shuffled_filename)
    
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    else:
        framerate = cap.get(5)
        #vid_width = int(cap.get(3)/2)
        #vid_height = int(cap.get(4)/2)

    # Read until video is completed
    line2 = make_fixationpoint(np.zeros((600,800,3))) 
    cv2.imshow('cap', line2)
    cv2.waitKeyEx(500)
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, frame = cap.read()       
        
        k = -1
        if ret == True:
            capname = "cap"
            
            line2 = make_fixationpoint(frame)
    
            #Display the resulting frame
            cv2.namedWindow(capname, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(capname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            #cv2.imshow(capname, frame)
            cv2.imshow(capname, line2)
            
            if cv2.waitKeyEx(int(1000/framerate)) != -1:
                time.sleep(1/framerate)
            
      # Break the loop
        else: 
            break
    
    cap.release()
    if k != Forwardkey and k != Backwardkey:
        k = checks_which_key('blank_image.png', [Forwardkey, Backwardkey])
        
    if k == Forwardkey:
        answer = 'Forward'
    if k == Backwardkey:
        answer = 'Backward'

    if sample['fwd/bckwd'] == answer:
        sample['answer'] = 1
    else:
        sample['answer'] = 0
        
    sample['time'] =  time.ctime()
    columns_df.append(sample).to_csv(data_filename, mode='a',header=False) 
    #data_df = data_df.append(sample)
    
show_image('all_done.png')
cv2.waitKeyEx(0)
cv2.destroyAllWindows()


datapath = 'run_directory'

data_df.to_csv(datapath+  'Data ' + subjectname +'.csv', mode = 'a')


# ### Plotting the data!! :)

# In[ ]:


import matplotlib
import matplotlib.pyplot as plt
from pandas.plotting import *


# In[ ]:


datapath = '/Users/phosphene/Documents/LynnDirectory/Biological Stimulations Frame Durations/experiment data/'

#Biological Stimulations Frame Durations/experiment data/

old_dataframe = pd.read_csv(datapath+'Biological Stimulations Frame DurationsData .csv')
new_dataframe = old_dataframe[['answer','frame duration in ms']]
new_dataframe['frame_duration'] =  new_dataframe['frame duration in ms']

print new_dataframe['frame_duration']

new_dataframe = new_dataframe.groupby((['frame_duration'])).mean()

new_dataframe = new_dataframe.sort_index(ascending = True)

new_dataframe = new_dataframe.drop(['frame duration in ms'], axis = 1)
new_dataframe.plot(legend = False)
plt.ylabel('fraction correct')
plt.title('Frame Duration Experiment Results:' + subjectname)

new_dataframe


# In[ ]:


# Run this part to save the plot:

plt.savefig(subjectname + '.png')


# In[ ]:


'/Users/phosphene/Documents/LynnDirectory/Biological Stimulations Frame Durations/experiment data/Biological Stimulations Frame DurationsData.csv'


# In[ ]:


Users(/phosphene/Documents/LynnDirectory/Biological, Stimulations, Frame, Durations/experiment, data/Biological, Stimulations, Frame, DurationsData, .csv)

