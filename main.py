#!/usr/bin/env python
# coding: utf-8




# Necessary Library Files

import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer





# Root Window and Its Properties
root = tk.ThemedTk()
root.get_themes()                 
root.set_theme("radiance")
root.geometry('885x550')
root.title("SpeakerBox")
root.iconbitmap(r'images/speakerbox.ico')




# Creating Status Bar

statusbar = ttk.Label(root, text="Welcome to Speaker Box", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)




# Functions Related to Menu Bar

def browse_file():
    global filename_path
    filename_path=""
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)
    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1

def about_us():
    tkinter.messagebox.showinfo('About SpeakerBox', 'This is a music player build using Python Tkinter by Kishlay Kishore, Tavish Gupta,')




# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)                #Assigns menubar as MENU of the root window

# Create the submenu
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="More", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)




playlist =[]




# Creating Frames
leftframe = Frame(root,width=300,height=500,borderwidth=5,bg="#FBB091")
leftframe.pack(side=LEFT,fill=X)

middleframe = Frame(root,width=400,height=500,borderwidth=5,bg="#91E1FB")
middleframe.pack(side=LEFT,fill=X)

"""rightframe = Frame(root,width=300,height=500,borderwidth=5,bg="#A8F8B5")
rightframe.pack(side=LEFT,fill=X)"""





mixer.init()                    #Initialising the Mixer




# LEFT FRAME




# Functions related to Left Frame

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)




# Elements in Left Frame
playlist_label= Label(leftframe,text="Curently Playing",width=45,height=3)
playlist_label.pack()

playlistbox = Listbox(leftframe,width=45,height=22)
playlistbox.pack()

addPhoto = PhotoImage(file='images/music.png')
addBtn = Button(leftframe, image=addPhoto, command=browse_file,bg="#FBB091")
addBtn.pack(side=LEFT,padx=20,pady=3)

delPhoto = PhotoImage(file='images/trash.png')
delBtn = Button(leftframe, image=delPhoto, command=del_song,bg="#FBB091")
delBtn.pack(side=RIGHT,padx=20,pady=3)




# MIDDLE FRAME




# Functions related to Middle Frame
def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1
        
            


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            nameLabel.configure(text=os.path.basename(play_it))
            show_details(play_it)
            
        except:
            #tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')
            print("not found file")


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE




# Elements in Middle Frame 
wavePhoto = PhotoImage(file='images/sound-waves.png')
display=Button(middleframe,image=wavePhoto,width=200,height=200)
display.pack(side=TOP)

song_name= "No SONG PLAYING"
nameLabel = ttk.Label(middleframe,text=song_name,width=45,relief=GROOVE)
nameLabel.pack()

middleframe_middle = Frame(middleframe,bg="#91E1FB")
middleframe_middle.pack(pady=30)

currenttimelabel = ttk.Label(middleframe_middle, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.grid(row=0, column=0, padx=10)

lengthlabel = ttk.Label(middleframe_middle, text='Total Length : --:--')
lengthlabel.grid(row=0, column=2, padx=10)

playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(middleframe_middle, image=playPhoto, command=play_music)
playBtn.grid(row=1,column=0, padx=10,pady =5)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe_middle, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=1,column=1, padx=10,pady=5)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe_middle, image=stopPhoto, command=stop_music)
stopBtn.grid(row=1, column=2, padx=10)


bottomframe_middle = Frame(middleframe)
bottomframe_middle.pack(pady=5)

mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(bottomframe_middle, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=0)

scale = ttk.Scale(bottomframe_middle, from_=0, to=100, orient=HORIZONTAL, command=set_vol,length=200)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=1, pady=15, padx=30)




# RIGHT FRAME




# Functions in Right Frame

def search():
    print("search")
    
def play_ml():
    print("play")
    s1_val=s1_scale.get()
    s2_val=s2_scale.get()
    s3_val=s3_scale.get()
    print(s1_val,s2_val,s3_val)
    


# Elements in Right Frame
topframe_right= Frame(rightframe)
topframe_right.pack(pady=5)

search_text=Entry(topframe_right,bg="pink",fg="#161BEE",font=("Comic Sans MS",15),width=20)
search_text.pack(side=LEFT)

search_btn=Button(topframe_right,text="Search",relief=GROOVE,command=search,bg="pink")
search_btn.pack()


midframe_right= Frame(rightframe,height=50)
midframe_right.pack()
searchlistbox = Listbox(midframe_right,width=45,height=10)
searchlistbox.pack()

label_ml= Label(midframe_right,text="Play My Mood",width=20,bg="#52C80D",borderwidth=4)
label_ml.pack()

bottomframe_right= Frame(rightframe,height=50)
bottomframe_right.pack(pady=5)

s1_scale= Scale(bottomframe_right,from_=10, to=-10)
s1_scale.grid(row=0,column=0,padx=30,pady=5)


s2_scale= Scale(bottomframe_right,from_=10, to=-10)
s2_scale.grid(row=0,column=1,padx=30,pady=5)


s3_scale= Scale(bottomframe_right,from_=10, to=-10)
s3_scale.grid(row=0,column=2,padx=30,pady=5)


label1= Label(bottomframe_right,text="Mood")
label1.grid(row=1,column=0,padx=30,pady=5)

label2= Label(bottomframe_right,text="Energy")
label2.grid(row=1,column=1,padx=30,pady=5)

label3= Label(bottomframe_right,text="Tune")
label3.grid(row=1,column=2,padx=30,pady=5)

ml_playPhoto = PhotoImage(file='images/play-button.png')
ml_playBtn = ttk.Button(bottomframe_right, image=ml_playPhoto, command=play_ml)
ml_playBtn.grid(row=2,column=1, padx=10,pady =5)




def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()


# In[ ]:




