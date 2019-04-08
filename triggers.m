% A script for implementing binary audio triggers in video stimuli for EEG recordings
% You must already have FFmpeg installed for this to work
% You also need a .csv file containing the identifiers of all your files, and the time(s) in ms
% that you want the trigger(s) to be.
% For each ID in the file, it reads the length of the video, creates a .wav audio track 
% that is all 0 except for the 50ms before the moment where you want your trigger (where 
% it is 1 instead). It then calls FFmpeg to combine the video and audio files, and deletes
% the .wav file as it is no longer necessary.

% Do we want multiple channels for triggers in different dimensions?

%%
% Set defaults
fs = 96000;
triggerLen = 0.05; % s

vidFiles = readtable('vidFiles.csv','Delimiter','\t'); % read in trigger file
for i = 1:height(vidFiles)
    file = vidFiles.fileId{i};
    vid = VideoReader([file,'.mp4']);
    vidDuration = vid.D; % retrieve video length
    audio = zeros(round(vidDuration * fs), 1); % initialize null audio
    tTimes = strsplit(vidFiles.trigTimes{1},','); %separate string if it contains multiple times
    for trigTime = tTimes
        trigTime = str2double(trigTime{1});
        audio(round(trigTime*fs - triggerLen*fs):round(trigTime*fs),1) = 1;% add 50ms trigger with offset at onset of sign
    end
    audFile = [file,'t.wav']; 
    audiowrite(audFile,audio,fs); % save audio track
    % Combine .mp4 and .wav file into 1 .avi file
    system(['ffmpeg -i ', file,'.mp4 -i ', file,'t.wav -map 0:0 -map 1:0 -vcodec copy -acodec copy ', file, 'Trig.avi']);
    delete(audFile); % delete .wav file
end
