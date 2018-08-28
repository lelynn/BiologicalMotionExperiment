%{
The StickfigureGenerator code produces stickfigure stimuli with the frame
durations 200, 160, 120, 80 and 40. Each containing a forward and backward
walker, and each one of those containing a forward and backward walker.
Each one of these videos can start with a different frame number (walker
position).
%}

Screen('Preference', 'SkipSyncTests', 1)
rng(1)

try
    dotsize = 5;
    connectionsize = 5; % max 7
    headsize = 23 ;
    headline = 5;
    %skel = [2 3 ; 3 4 ; 5 6 ; 6 7 ; 8 9 ; 9 10 ; 11 12 ; 12 13 ];
    skel = [1 1 ;2 2;3 3; 4 4; 5 5;6 6; 7 7 ; 8 8 ; 9 9 ; 10 10; 11 11 ; 12 12; 13 13];
    %defines the lines between the dots in skel
    connections = [2 3;3 4;5 6;6 7; 8 9;9 10;11 12;12 13];
    %connections = [2 3;3 4;5 6;6 7;8 9;9 10;11 12;12 13;2 5;8 11;2 8;5 11];
    %1 = head
    %2 = left shoulder
    %3 = left elbow
    %4 = left hand
    %5 = right shoulder
    %6 = right elbow
    %7 = right hand
    %8 = 1hip
    %9 = knee
    %10 = foot
    %11 =2hip
    %12 = knee  
    %13 = foot

    bm = BioMotion('BiomotionToolbox/BioMotionToolboxDemos/actions/walker.txt');

    bm.Loop = 1;
    bm.Rotation = pi/2;
    bm.SetRotation(pi/2);
    bm.Scale = 1.24; 
    
    %Limited Lifetime, dots drawm along limb segments (c.f. Beintema &
    %Lappe (2002)
    %skel = []
    bm.Skeleton = skel;
    %ndots = dots per frame maxlife = lifetime in frames
    bm.SetLimitedLifeParameters('ndots',13,'maxlife',1);

    %Limited lifetime, dots drawn on joints only, Need to decrease 'ndots;
    %to <nPointLights, in order tp seee the effect
    %ndots = dots per frame maxlife = lifetime in frames
    SetAll(bm, 'LimitedLife', 1);

    win = SetScreen('OpenGL', 1);
    SetProjection(win);

    %startfrno = 1;
    %framerate = 30;
    %dration = 120;
    dration = 120;
    screencenter = get(0,'screensize');
    screencenter = screencenter(3:4)'/2;       
    runtimecounter = 0;
    for frate = 1000./[200 160 120 80 40] % For loop for different frame durations
        
        for ismirror = [true false] %for loop for original and mirrored facing direction
            if ismirror
                moname = 'Mirror';
            else 
                moname = 'Orig';
            end
            for isback = [true false] %for loop for forward and backward walking direction
                if isback
                   bfname = 'Rev';
                else
                   bfname = 'Fwd';
                end
            
                %start frame number loop
                for startfrno = ceil((0:9)*(133/10) + (rand*13)) %for loop for different starting positions

                    %set frames per second with frate:
                    %adjust the framerate here (Hz)  
                    %save video file name in strcat() (frame rate is converted to frame
                    %duration
                    myVideo = VideoWriter(strcat(bfname, moname, num2str(1000/frate), '[', num2str(startfrno), ']'), 'MPEG-4');
                    myVideo.FrameRate = frate; 

                    %video must be opened before written
                    open(myVideo);

                    for fr = (60/frate)*(startfrno:(startfrno+dration/(60/frate))) %to make sure each video is evenly long

                        while KbCheck

                            throw "stop"
                        end
                        if isback %how the backward walker is made (reversing frame order)
                            fr = 120 - fr; 
                        end
                        
                        %if framerate is a whole number
                        if floor(fr) ==  fr
                            frame = bm.GetFrame(fr)
                        %if framerate is not a whole number, the weighted
                        %averaging is performed.
                        else
                            weight = fr - floor(fr);
                            frame1 = bm.GetFrame(floor(fr));
                            frame2 = bm.GetFrame(ceil(fr));
                            frame = frame1 * (1 - weight) + (frame2 * weight);
                        end
                        
                        if ismirror %multiplying the frame by this matrix allows a mirrored image.
                            frame = frame.* [-1, 1, 1]'
                        end
                        
                        % To move the frame to the lower left, activate
                        % this comment below.
                        %frame = frame + [-100; -75; 0]

                        %fill lines matrix with all wanted lines bewteen dots
                        %frame(1,a) is x coordinate
                        %frame(2,a) is y coordinate
                        lines = [];
                        for conn = connections'
                            lines = [lines;
                                frame(1,conn(1)) frame(2,conn(1)); 
                                frame(1,conn(2)) frame(2,conn(2))];
                        end

                        %add a line from the head to the center of the shoulders
                        shoulder_average_x = (frame(1,2) + frame(1,5))/2
                        shoulder_average_y = (frame(2,2) + frame(2,5))/2
                        
                        head_x = frame(1,1)
                        head_y = frame(2,1)
                        
                        lines = [lines; 
                            head_x head_y;
                            sholder_average_x shoulder_average_y];

                        %add a line from the center of sholders to the center of the hips
                        hip_average_x = (frame(1,8) + frame(1,11))/2
                        hip_average_y = (frame(2,8) + frame(2,11))/2
                        lines = [lines; 
                            shoulder_average_x shoulder_average_y;
                            hip_average_x hip_average_y];


                        %The DrawLines functionality uses opposite y direction and
                        %differend 0,0 coordinate. The following is to correct this and to 
                        %align the lines with the dots. This also transposes lines to get 
                        %the correct shape for DrawLines.
                        lines = lines' .*[1 ;-1] + screencenter;

                        %draw lines on screen
                        Screen('DrawLines',win.Number,lines,connectionsize, [255 255 255]);
                        circle_rect = [head_x-headsize/2 head_x+headsize/2; head_y head_y+headsize] .* [1; -1] + screencenter
                        
                        %Screen('FrameOval',win.Number,[255 255 255],circle_rect, headline)
                        Screen('FillOval',win.Number,[255 255 255],circle_rect, headsize+1)
                        
                        %draw dots on screen
                        moglDrawDots3D(win.Number, frame, dotsize,[],[], 2);
                        Screen('Flip', win.Number);
                        
                        %write screen to file
                        writeVideo(myVideo, Screen('GetImage', win.Number, win.Rect))

                    end
                    close(myVideo)
                end
            end
        end
    end
        clear screen;
        
catch ME 
    clear screen;
    rethrow (ME);
end

%calculating the pixels
global_max = [0 0 0]
global_min = [0 0 0]
for f = 1:200
    frame = bm.GetFrame(f)
    
    global_max = max([max(frame'); global_max])
    global_min = min([min(frame'); global_min])
end
    