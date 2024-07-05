import pygame
import os
from tkinter import *
from tkinter import filedialog

pygame.mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("600x400")
        
        #track frame
        self.track_frame = LabelFrame(self.root, text="Song Track", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5, relief=GROOVE)
        self.track_frame.place(x=0, y=0, width=600, height=100)
        
        #track name
        self.track_name = StringVar()
        self.track_label = Label(self.track_frame, textvariable=self.track_name, width=35, font=("times new roman", 24, "bold"), bg="grey", fg="gold")
        self.track_label.grid(row=0, column=0, padx=10, pady=5)
        
        #control frame
        self.control_frame = LabelFrame(self.root, text="Control Panel", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5, relief=GROOVE)
        self.control_frame.place(x=0, y=100, width=600, height=100)
        
        #load button
        self.load_button = Button(self.control_frame, text="Load Songs", width=10, height=1, font=("times new roman", 16, "bold"), fg="navyblue", bg="white", command=self.load_songs)
        self.load_button.grid(row=0, column=0, padx=10, pady=5)
        
        #play button
        self.play_button = Button(self.control_frame, text="Play", width=10, height=1, font=("times new roman", 16, "bold"), fg="navyblue", bg="white", command=self.play_song)
        self.play_button.grid(row=0, column=1, padx=10, pady=5)
        
        #pause button
        self.pause_button = Button(self.control_frame, text="Pause", width=10, height=1, font=("times new roman", 16, "bold"), fg="navyblue", bg="white", command=self.pause_song)
        self.pause_button.grid(row=0, column=2, padx=10, pady=5)
        
        #stop button
        self.stop_button = Button(self.control_frame, text="Stop", width=10, height=1, font=("times new roman", 16, "bold"), fg="navyblue", bg="white", command=self.stop_song)
        self.stop_button.grid(row=0, column=3, padx=10, pady=5)
        
        #Listbox frame
        self.listbox_frame = LabelFrame(self.root, text="Playlist", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5, relief=GROOVE)
        self.listbox_frame.place(x=0, y=200, width=600, height=200)
        
        #Listbox for songs loaded
        self.playlist = Listbox(self.listbox_frame, selectbackground="gold", selectmode=SINGLE, font=("times new roman", 12, "bold"), bg="silver", fg="navyblue", bd=5, relief=GROOVE)
        self.playlist.grid(row=0, column=0, padx=10, pady=5)
        
        #scrollbar
        self.scrollbar = Scrollbar(self.listbox_frame, orient=VERTICAL)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.playlist.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.playlist.yview)

    def load_songs(self):
        self.song_files = filedialog.askopenfilenames(initialdir="C:/", title="Choose A Song", filetype=(("mp3 Files", "*.mp3"), ))
        for song in self.song_files:
            self.playlist.insert(END, os.path.basename(song))
        
    def play_song(self):
        self.current_song = self.playlist.get(ACTIVE)
        self.track_name.set(self.current_song)
        pygame.mixer.music.load(self.song_files[self.playlist.curselection()[0]])
        pygame.mixer.music.play()
        
    def pause_song(self):
        pygame.mixer.music.pause()
        
    def stop_song(self):
        pygame.mixer.music.stop()

root = Tk()
app = MusicPlayer(root)
root.mainloop()
