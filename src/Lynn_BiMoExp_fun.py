import cv2
import numpy as np
import time
import os
import pandas as pd
from sklearn.utils import shuffle
import sys

#These are the simulation videos that are put into a dataframe (videos_df). There are a total of 20 unique videos and will eventually be shuffled the order and multiplied 5 times. 
class Running_experiment():
        

    def __init__(self):
        '''The class Experiment, '''
        self.run_directory = '../'
        # self.set_experiment(experiment)
    
    def set_experiment(self, experiment):
        ''' 
        Experiments available
        ---------------------
        Dotfigure_center

        Phosphenefigure_center

        Dotfigure_LLQ
        
        Phosphenefigure_LLQ '''

        self.experiment = experiment
        self.experiment_directory = self.run_directory + 'experiment/' + self.experiment
        self.video_path = self.experiment_directory + '/FinalVideos/'
    

    def videos_to_pd(self):
        ''' The function videos_to_pd() takes all the FinalVideos in the provided 
        experiment_directory and organizes it into a pandas DataFrame. 
        
        The FinalVideos the experiment_directory must be organized in certain maps. 
        First, '/Forward' and '/Reverse' maps, and in each of those maps there are
        '/Original' and '/Mirror' maps.
        
        This function calls those videos from each map and writes it into a data frame, returning a videos_df.
        
        Parameters
        ----------
        The parameter is a string representing the experiment name that will be called.
        
        Dotfigure_center: presents the simulation videos of the dotfigures on the center of the screen
        
        Dotfigure_LLQ: presents the simulation videos of the dotfigures on the LLQ of the screen
        
        Phosphenefigure_center: presents the simulation videos of the phosphenefigures on the center of the screen
        
        Phosphenefigure_LLQ: presents the simulation videos of the phosphenefigures on the LLQ of the screen
        
        '''

        self.videos_df = pd.DataFrame(columns=['filename','fwd/bckwd', 'm/o', 'frame duration in ms'])

        for v in os.listdir(self.video_path+'Forward/Original'):
            if v.endswith('.mp4'):
                self.videos_df = self.videos_df.append({'filename':'Forward/Original/'+v,'fwd/bckwd': "Forward", 'm/o': "o", 'frame duration in ms': v[7:v.find('[')]},ignore_index=True)

        for v in os.listdir(self.video_path+'Forward/Mirror'):
            if v.endswith('.mp4'):
                self.videos_df = self.videos_df.append({'filename':'Forward/Mirror/'+v,'fwd/bckwd': "Forward", 'm/o': "m", 'frame duration in ms': v[9:v.find('[')]},ignore_index=True)

        for v in os.listdir(self.video_path+'Reverse/Mirror'):
            if v.endswith('.mp4'):
                self.videos_df = self.videos_df.append({'filename':'Reverse/Mirror/'+v,'fwd/bckwd': "Backward", 'm/o': "o", 'frame duration in ms': v[9:v.find('[')]},ignore_index=True)

        for v in os.listdir(self.video_path+'Reverse/Original'):
            if v.endswith('.mp4'):
                self.videos_df =self.videos_df.append({'filename':'Reverse/Original/' +v ,'fwd/bckwd': "Backward", 'm/o': "m", 'frame duration in ms': v[7:v.find('[')]},ignore_index=True)
     
        return self.videos_df


    def play_two_demovids(self, demovid_filename1):
        ''' This function presents the demonstration videos from the map /Demo Videos/ of the experiment_directory.
        
        Parameters
        ----------
        Demonstration videos are showed before subjects are doing the tasks. Each expriment has its own /Demo Video/ map which shows the subjects what they can expect during the experiment. 
        
        'FwdMirror60demo.mp4': this is the filename of the demonstration video for the walker going forward, facing the mirrored way, at  60 frame duration.
        
        'FwdOrig60demo.mp4': this is the filename of the demonstration video for the walker going forward, facing the original way, at  60 frame duration.
        
        'RevMirror60demo.mp4': this is the filename of the demonstration video for the walker going backward, facing the mirrored way, at  60 frame duration.
        
        'RevOrig60demo.mp4': this is the filename of the demonstration video for the walker going backward, facing the original way, at  60 frame duration.
        
        '''
        path_to_demovid = self.experiment_directory + '/Demo Videos/'
        cap = cv2.VideoCapture(path_to_demovid + demovid_filename1)
        
        if (cap.isOpened()== False): 
            print("Error opening video stream or file")
        else:
            framerate = cap.get(5)
        # Read until video is completed
        while(cap.isOpened()):
        # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True: 
                self.make_fixationpoint(frame)
                capname = "cap"
                #allows the resizing and centering of the video window:
                cv2.namedWindow(capname, cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty(capname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow(capname, frame)
                cv2.waitKeyEx(40)
            else: 
                break


    def show_image(self, image_filename):
        ''' The function show_image() takes the monitor and shows the image WITH fixation point (see make_fixationpoint() doc)
            show_image is also used in the checks_which_key() funtion, a recursion to check keys and force key presses.
            
        Parameter
        ---------
        Use the images filename in the map of run_directory + '/Introduction/Images/'. 
        
        '''
        path_to_img =  self.run_directory + '/Introduction/Images/'

        img = cv2.imread(path_to_img + image_filename)
        line2 = self.make_fixationpoint(img)
        winname = "cap"
        cv2.namedWindow(winname, cv2.WND_PROP_FULLSCREEN)          
        cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(winname,line2)

    def determine_keys(self):
        ''' Function that allows the keys to be determined for the experiment. 
        Key response are the ones that will be used in the experiment to indicate forward or backward
        This function returns a tuple of 3 keys: Forwardkey, Backwardkey, and Continuekey. 
        When calling the function, the tuple needs to be separated'''
        
        self.show_image('indicate_forward.png')
        self.Forwardkey = cv2.waitKeyEx(0)

        #Determining the 'backward' Key
        self.show_image('indicate_backward.png')
        self.Backwardkey = cv2.waitKeyEx(0)

        #Determining the 'continue' Key
        self.show_image('indicate_continue.png')
        self.Continuekey = cv2.waitKeyEx(0)
        
    def show_task(self):
        self.show_image('Your_task.png')
        cv2.waitKeyEx(0) 

    def run_test(self):
        ''' This function allows subjects to respond to stimuli with keys without saving any data. 
        This is so that the subjects may get used to the experiment. 
        
        This function returns 10 different videos each time.
        '''
        shuffled_test_samples = shuffle(self.videos_df.head(10))

        for i, sample in shuffled_test_samples.iterrows():
        
            shuffled_filename = sample['filename']

            cap = cv2.VideoCapture(self.video_path + shuffled_filename)

            if (cap.isOpened()== False): 
                print("Error opening video stream or file")
            else:
                framerate = cap.get(5)

            # Read until video is completed
            line2 = self.make_fixationpoint(np.zeros((600,800,3))) 
            cv2.imshow('cap', line2)
            cv2.waitKeyEx(500)
            while(cap.isOpened()):
            # Capture frame-by-frame
                ret, frame = cap.read()       
                if ret == True:
                    capname = "cap"

                    line2 = self.make_fixationpoint(frame)

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
            if k != self.Forwardkey and k != self.Backwardkey:
                k = self.checks_which_key('blank_image.png', [self.Forwardkey, self.Backwardkey])

    def checks_which_key(self, image_filename, which_keys, wait_key_ms = 0):
        '''The function shows an image, then waits for a key response. If it is [one of] the expected keys, then it 
        will repeat. If the key response is not expected, then the try_again image is shown.
        Subject is forced to try until expected key is pressed. 
        
        Parameters
        ----------
        
        image_filename: insert the filename of the image that you want to present to the subject. For example 'press the F key'
        
        which_keys: this is defined from the determine_keys(), see doc 
        
        wait_keys_ms = 0'''
        
        self.show_image(image_filename)
        which_key_check = cv2.waitKeyEx(wait_key_ms)
        if which_key_check in which_keys:
            return which_key_check
        else:
            self.show_image('try_again.png')
            cv2.waitKey(500)
            return self.checks_which_key(image_filename, which_keys)
        

    def make_fixationpoint(self, img):
        '''Creates a red fixation cross on the image by taking the exact half of the imag dimensions and using +/- 5 pixels to produce the cross.
        
        parameter
        ---------
        img: the image to be shown on screen with red fixatoin cross.'''
        
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

    def teaching_forward(self):
        ''' This function shows the images and demovideos in order to demonstrate a forward walker.
        Also it tests whether subject understands the key that needs to be pressed when seeing this stimulus.'''
        self.show_image('Forward_before.png')
        cv2.waitKeyEx(0)
        self.play_two_demovids('FwdMirror60demo.mp4')
        self.play_two_demovids('FwdOrig60demo.mp4') 

        #FORWARD DEMOVID
        #check_forward_press
        self.checks_which_key('Forward_after.png', [self.Forwardkey])
        self.show_image('well_done.png')
        cv2.waitKey(500) 
    
    def teaching_backward(self):
        ''' This function shows the images and demovideos in order to demonstrate a backward walker.
        Also it tests whether subject understands the key that needs to be pressed when seeing this stimulus.'''

        self.show_image('Backward_before.png')
        cv2.waitKeyEx(0)

        self.play_two_demovids('RevMirror60demo.mp4')
        self.play_two_demovids('RevOrig60demo.mp4')

        self.checks_which_key('Backward_after.png', [self.Backwardkey])
        self.show_image('well_done.png')
        cv2.waitKey(500)

    def run_experiment(self, subjectname):
        ''' Run the experiment with subject name as parameter. The data will also be saved as the subject name into the experiment data folder.
        The data is saved after each loop, therefore quitting the experiment midrun does not cause loss of all data.
        '''
        datapath =  self.run_directory + '/experiment data/'
        data_filename = datapath+subjectname+'.csv'

        columns_df = pd.DataFrame(columns=["filename", 
                                        "fwd/bckwd", 
                                        "m/o", 
                                        "frame duration in ms", 
                                        "answer", 
                                        "time"])    
        columns_df.to_csv(data_filename, mode='a')



        shuffled_samples = shuffle(self.videos_df
                                )
        pausecounter = 50

        for i, sample in shuffled_samples.iterrows():

            if pausecounter == 0:

                self.checks_which_key('continue.png', [self.Continuekey], 120000)
            # while cv2.waitKeyEx(120000) != Continuekey: #break 2 minutes
                    #show_image('continue.png')
                pausecounter = 50
            else:
                pausecounter -= 1

            shuffled_filename = sample['filename']

            cap = cv2.VideoCapture(self.video_path + shuffled_filename)

            if (cap.isOpened()== False): 
                print("Error opening video stream or file")
            else:
                framerate = cap.get(5)
                #vid_width = int(cap.get(3)/2)
                #vid_height = int(cap.get(4)/2)

            # Read until video is completed
            line2 = self.make_fixationpoint(np.zeros((600,800,3))) 
            cv2.imshow('cap', line2)
            cv2.waitKeyEx(500)
            while(cap.isOpened()):
            # Capture frame-by-frame
                ret, frame = cap.read()       

                k = -1
                if ret == True:
                    capname = "cap"

                    line2 = self.make_fixationpoint(frame)

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
            # The following tests whether the response was correct 
            if k != self.Forwardkey and k != self.Backwardkey:
                k = self.checks_which_key('blank_image.png', [self.Forwardkey, self.Backwardkey])

            if k == self.Forwardkey:
                answer = 'Forward'
            if k == self.Backwardkey:
                answer = 'Backward'

            if sample['fwd/bckwd'] == answer:
                sample['answer'] = 1
            else:
                sample['answer'] = 0

            sample['time'] =  time.ctime()
            columns_df.append(sample).to_csv(data_filename, mode='a',header=False) 

        self.show_image('all_done.png')
        cv2.waitKeyEx(0)
        cv2.destroyAllWindows()
        

if __name__ == '__main__':

    rne = Running_experiment()
    rne.set_experiment('Dotfigure_LLQ')
    videos_df = rne.videos_to_pd()

    #Determine the keys
    rne.determine_keys()
    #Show what is forward
    rne.teaching_forward()
    #Show what is backward
    rne.teaching_backward()
    #show the task
    rne.show_task()   
    #run 10 testruns
    rne.run_test()

    #run the actual experiment (with subject's name as parameter) and collect data
    rne.run_experiment('testing_1')
    #saving the data into the path
    datapath = 'run_directory'
    rne.data_df.to_csv(datapath+  'Data ' + subjectname +'.csv', mode = 'a')