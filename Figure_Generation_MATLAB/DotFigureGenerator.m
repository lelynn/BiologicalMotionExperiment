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
    dotsize = 3
    skel = [2 3 ; 3 4 ; 5 6 ; 6 7 ; 8 9 ; 9 10 ; 11 12 ; 12 13 ]
    %skel = [1 1; 2 2;3 3; 4 4; 5 5; 7 7 ; 8 8 ; 9 9 ; 10 10; 11 11 ; 12 12; 13 13]
    %1 = head
    %2 = left shoulder
    %3 = left elbow
    %4 = left hand
    %5 = right shoulder
    %6 = right elbow
    %7 = right hand
    %8 = 1hipdsa
    %9 = knee
    %10 = foot
    %11 =2hip
    %12 = knee  
    %13 = foot

    bm = BioMotion('BiomotionToolbox/BioMotionToolboxDemos/actions/walker.txt');

    bm.Loop = 1
    bm.Rotation = pi/2;
    bm.Scale = 1.24; 

    %Limited Lifetime, dots drawm along limb segments (c.f. Beintema &
    %Lappe (2002)
    %skel = []
    bm.Skeleton = skel;
    bm.SetLimitedLifeParameters('ndots',8,'maxlife',1);

    %Limited lifetime, dots drawn on joints only, Need to decrease 'ndots;
    %to <nPointLights, in order tp seee the effect
    %ndots = dots per frame maxlife = lifetime in frames
    SetAll(bm, 'LimitedLife', 1);

    win = SetScreen('OpenGL', 1);
    SetProjection(win);
    for frate = 1000./[200 160 120 80 40] %for loop for different frame rates
    
        for ismirror = [true false] %for loop for original and mirrored facing direction
            if ismirror
                moname = 'Mirror';
            else 
                moname = 'Orig';
            end
            %backward or forward
            for isback = [true false] % for loop for backward and forward
                if isback
                    bfname = 'Rev';
                else
                    bfname = 'Fwd';
                end

                %start frame number:
                for startfrno = ceil((0:9)*(133/10) + (rand*13))

                    %set frames per second with frate:
                    %adjust the framerate here (Hz)  
                    %save video file name in strcat() (frame rate is converted to frame
                    %duration
                    myVideo = VideoWriter(strcat(bfname, moname, num2str(1000/frate), '[', num2str(startfrno), ']'), 'MPEG-4');
                    myVideo.FrameRate = frate; 

                    %video must be opened before written
                    open(myVideo);

                    for fr = (60/myVideo.FrameRate)*(1:(120/(60/myVideo.FrameRate)))+startfrno %ensures evenly long videos

                        while KbCheck
=
                            throw "stop"
                        end
                        
                        if isback
                            fr = 120 - fr;
                        end
                        
                        if floor(fr) == fr % if frame is a whole number, then continue normally
                            frame = bm.GetFrame(fr)
                        else
                            weight = fr - floor(fr); %if framerate is not a whole number, the weighted
                        %averaging is performed.
                            frame1 = bm.GetFrame(floor(fr));
                            frame2 = bm.GetFrame(ceil(fr));
                            frame = frame1 * (1 - weight) + (frame2 * weight);
                        end
                        
                        if ismirror
                            frame = frame.* [-1, 1, 1]' 
                        end
                        
                        %LLQ, comment the following to center the stimuli on the screen:
                        frame = frame + [-100; -75; 0]
                        
                        moglDrawDots3D(win.Number, frame, dotsize ,[],[], 2); 
                        %writeVideo code is to save video
                        writeVideo(myVideo, Screen('GetImage', win.Number, win.Rect))
                        Screen('Flip', win.Number);
                    end       
                end
            end
        end
    end
    
    clear screen
    close(myVideo)
    
catch ME 
    clear screen
    rethrow (ME);
end

        
    