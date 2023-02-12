import urllib.request
import re
from pytube import YouTube
import os
import imageio
try:
    imageio.plugins.ffmpeg.download()
except:
    print("Instal imageio==2.4.1")
    exit(1)
from moviepy.editor import *
import sys
import zipfile
input_args = sys.argv
if len(input_args) != 5:
    print("Invalid number of arguments")
    exit(1)
name = input_args[1]
num_videos = input_args[2]
cut_duration = input_args[3]
output_file = input_args[4]
singer = name.replace(' ', '+')

if output_file.count('.') == 0:
    output_file += '.wav'
output_file.split('.')[-1] = 'wav'



num_of_videos = int(num_videos)

def get_videos(singer):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + singer)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    temp_videos = ["https://www.youtube.com/watch?v=" + video_id for video_id in video_ids]
    print(len(temp_videos))
    #make list values unique
    temp_videos = list(set(temp_videos))
    print(len(temp_videos))
    videos = []
    idx = 1
    for video in temp_videos:
        if idx > num_of_videos:
            break
        yt = YouTube(video)
        if yt.length/60 < 5.00:
            videos.append(video)
            idx += 1
    return videos


def download_video(video):
    downloadPath = 'videos/'
    if not os.path.exists(downloadPath):
        os.makedirs(downloadPath)
    yt = YouTube(video)
    try :
        yt.streams.first().download(downloadPath)
    except :
        print("Error in downloading video")

def convert_vid_to_audio():
    SAVE_PATH = os.getcwd() + '/'
    #get paths of videos stored in videos folder using os module
    path = os.getcwd()+'/videos/'
    print(path)
    ds_store = path + ".DS_Store"
    if os.path.exists(ds_store):
        os.remove(ds_store)
    fileList = os.listdir(path)
    print(fileList)
    idx = 1
    if not os.path.exists(SAVE_PATH + 'audios/'):
        os.makedirs(SAVE_PATH + 'audios/')
    for file in fileList:
        print(file)
        video = VideoFileClip(path+file).subclip(0, int(cut_duration))
        video.audio.write_audiofile(SAVE_PATH + '/audios/' + str(idx) + ".mp3")
        video.close()
        os.remove(path+file)
        idx += 1

def mergeAudios():
    SAVE_PATH = os.getcwd() + '/'
    final_wav_path = SAVE_PATH + "audios/" + output_file
    ds_store = SAVE_PATH + "/audios/.DS_Store"
    if os.path.exists(ds_store):
        os.remove(ds_store)
    if os.path.exists(final_wav_path):
        os.remove(final_wav_path)
    for file in os.listdir(SAVE_PATH + "/audios/"):
        if file.endswith(".zip"):
            os.remove(SAVE_PATH + "/audios/" + file)
    wavs = os.listdir(SAVE_PATH + "/audios/")
    
    final_clip = concatenate_audioclips([AudioFileClip(SAVE_PATH + "/audios/"+wav) for wav in wavs])
    final_clip.write_audiofile(final_wav_path)
    final_clip.close()
    print("Done merging wavs to " + final_wav_path)

def zipAudio():
    SAVE_PATH = os.getcwd() + '/'
    final_wav_path = "audios/" + output_file
    zip_file = final_wav_path + ".zip"
    with zipfile.ZipFile(zip_file, 'w') as myzip:
        myzip.write(final_wav_path)

def clearFiles():
    path = os.getcwd()+'/audios/'
    path2 = os.getcwd()+'/videos/'
    if os.path.exists(path) and os.path.exists(path2):
        fileList = os.listdir(path)
        for file in fileList:
            os.remove(path+file)
        fileList = os.listdir(path2)
        for file in fileList:
            os.remove(path2+file)

  
        
    
    

clearFiles()
videos = get_videos(singer)
print(len(videos))
print('Get video links done \n')
for video in videos:
    print(video)
    download_video(video)
print("videos downloaded \n")
convert_vid_to_audio()
mergeAudios()
zipAudio()