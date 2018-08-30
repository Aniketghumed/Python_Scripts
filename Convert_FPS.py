import os
import shutil
import cv2
import sys
import subprocess
from subprocess import call

#Collecting arguments passed
into_fps=sys.argv[1]
video_path=sys.argv[2]
global fps

#Current directory
dir_path = os.path.dirname(os.path.realpath(__file__))

#Get the FPS of current video
video = cv2.VideoCapture(video_path)
if video.get(cv2.cv.CV_CAP_PROP_FPS):
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
else :
    fps = video.get(cv2.CAP_PROP_FPS)
video.release()

if not os.path.exists(dir_path+'/frames'):
        os.makedirs(dir_path+'/frames')

#Creating tempo for FFMPEG command
tempo=1/(fps/int(into_fps))

#Extracting frames of the video into frames folder of current directory
vidcap = cv2.VideoCapture(video_path)
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(os.path.join(dir_path+'/frames', "frame%d.jpg" % count), image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1

# COMMAND:- ffmpeg -framerate 20 -i /home/user/Desktop/part3/frame%01d.jpg -c:v libx264 -pix_fmt yuv420p -crf 23 /home/user/Desktop/part320.mp4
call(["ffmpeg","-framerate",into_fps,"-i",dir_path+'/frames/frame%01d.jpg',"-c:v","libx264","-pix_fmt","yuv420p","-crf","23",dir_path+'/noaudio'+str(into_fps)+'fps.mp4'])
shutil.rmtree(dir_path+'/frames')

# COMMAND:- ffmpeg -i test.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav
call(["ffmpeg","-i",video_path,"-ab","160k","-ac","2","-ar","44100","-vn",dir_path+'/originalaudio.wav'])

# COMMAND:- ffmpeg -i "25fpsvid.mp4" -i "audio.wav" -af atempo=0.83447503425 -c:v copy -c:a aac -strict -2 -b:a 128k output.mp4
call(["ffmpeg","-i",dir_path+'/noaudio'+str(into_fps)+'fps.mp4',"-i",dir_path+'/originalaudio.wav',"-af","atempo="+str(tempo),"-c:v","copy","-c:a","aac","-strict","-2","-b:a","128k","-strict","-2",dir_path+'/videowith'+str(into_fps)+'fpsaudio.mp4'])

# COMMAND:- ffmpeg -i test.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav
call(["ffmpeg","-i",dir_path+'/videowith'+str(into_fps)+'fpsaudio.mp4',"-ab","160k","-ac","2","-ar","44100","-vn",dir_path+'/'+str(into_fps)+'fpsaudio.wav'])

# COMMAND:- ffmpeg -i /home/user/Desktop/part120.mp4 -i /home/user/Desktop/part1-stretch.wav -vcodec copy -strict -2 /home/user/Desktop/final_parts/outputpart1.mp4
call(["ffmpeg","-i",dir_path+'/noaudio'+str(into_fps)+'fps.mp4',"-i",dir_path+'/'+str(into_fps)+'fpsaudio.wav',"-vcodec","copy","-strict","-2",dir_path+'/finaloutput.mp4'])

#Deleting intermediate data
os.remove(dir_path+'/noaudio'+str(into_fps)+'fps.mp4')
os.remove(dir_path+'/originalaudio.wav')
os.remove(dir_path+'/videowith'+str(into_fps)+'fpsaudio.mp4')
os.remove(dir_path+'/'+str(into_fps)+'fpsaudio.wav')
