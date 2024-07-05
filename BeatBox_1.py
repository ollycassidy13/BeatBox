import pygame
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

pygame.mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("BeatBox")
        self.root.minsize(800, 460)
        self.root.configure(bg='#ffffff')
        
        style = ttk.Style()
        style.configure('TFrame', background='#ffffff')
        style.configure('TButton', background='#d3d3d3', foreground='#333333', font=('Helvetica', 12))
        style.map('TButton', background=[('active', '#b0b0b0')])
        style.configure('TLabel', background='#ffffff', foreground='#333333', font=('Helvetica', 12))
        style.configure('TLabelFrame', background='#ffffff', foreground='#333333', font=('Helvetica', 12, 'bold'))
        style.configure('TListbox', background='#d3d3d3', foreground='#333333', font=('Helvetica', 12))

        # Track frame
        self.track_frame = ttk.LabelFrame(self.root, text="Song Track")
        self.track_frame.place(x=10, y=10, width=780, height=80)
        
        # Track name
        self.track_name = StringVar()
        self.track_label = ttk.Label(self.track_frame, textvariable=self.track_name, font=("Helvetica", 16))
        self.track_label.grid(row=0, column=0, padx=10, pady=20)
        
        # Control frame
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.place(x=10, y=100, width=780, height=80)
        
        # Load button
        self.load_button = ttk.Button(self.control_frame, text="Load Songs", command=self.load_songs)
        self.load_button.grid(row=0, column=0, padx=10, pady=20)
        
        # Play button
        self.play_button = ttk.Button(self.control_frame, text="▶", command=self.play_song)
        self.play_button.grid(row=0, column=1, padx=10, pady=20)
        
        # Pause button
        self.pause_button = ttk.Button(self.control_frame, text="||", command=self.pause_song)
        self.pause_button.grid(row=0, column=2, padx=10, pady=20)
        
        # Stop button
        self.stop_button = ttk.Button(self.control_frame, text="■", command=self.stop_song)
        self.stop_button.grid(row=0, column=3, padx=10, pady=20)

        # Skip button
        self.skip_button = ttk.Button(self.control_frame, text=">|", command=self.skip_song)
        self.skip_button.grid(row=0, column=4, padx=10, pady=20)

        # Remove button
        self.remove_button = ttk.Button(self.control_frame, text="Remove Song", command=self.remove_songs)
        self.remove_button.grid(row=0, column=5, padx=10, pady=20)
        
        # Listbox frame
        self.listbox_frame = ttk.LabelFrame(self.root, text="Queue")
        self.listbox_frame.place(x=10, y=200, width=780, height=250)
        
        # Listbox for songs loaded
        self.queue = Listbox(self.listbox_frame, selectbackground="gold", selectmode=SINGLE, font=("Helvetica", 12), bg="#d3d3d3", fg="#333333")
        self.queue.grid(row=0, column=0, ipadx=275, padx=10, pady=10)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.listbox_frame, orient=VERTICAL, command=self.queue.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.queue.config(yscrollcommand=self.scrollbar.set)

        self.song_files = []
        self.current_song = None
        self.is_paused = False
        self.selected_index = 0

        # Check for end of track event
        self.check_music_end()

    def load_songs(self):
        new_song_files = filedialog.askopenfilenames(initialdir="C:/", title="Choose A Song", filetype=(("mp3 Files", "*.mp3"), ))
        for song in new_song_files:
            if song not in self.song_files:  # To avoid duplicates
                self.song_files.append(song)
                self.queue.insert(END, os.path.basename(song))

    def remove_songs(self):
        selected_indices = self.queue.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            self.queue.delete(selected_index)
            del self.song_files[selected_index]
        
    def play_song(self):
        if self.is_paused and not self.queue.curselection():
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            if self.queue.curselection():
                self.selected_index = self.queue.curselection()[0]
            else:
                self.selected_index = 0
                self.queue.select_set(self.selected_index)
            
            if self.selected_index < len(self.song_files):
                self.current_song = self.queue.get(self.selected_index)
                self.track_name.set(self.current_song)
                pygame.mixer.music.load(self.song_files[self.selected_index])
                pygame.mixer.music.play()
                self.is_paused = False

        self.queue.selection_clear(0, END)
        
    def pause_song(self):
        pygame.mixer.music.pause()
        self.is_paused = True
        
    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_paused = False

    def skip_song(self):
        if self.selected_index + 1 < len(self.song_files):
            self.selected_index += 1
            self.queue.select_set(self.selected_index)
            self.current_song = self.queue.get(self.selected_index)
            self.track_name.set(self.current_song)
            pygame.mixer.music.load(self.song_files[self.selected_index])
            pygame.mixer.music.play()
            self.queue.selection_clear(0, END)
        else:
            self.selected_index = 0
            self.queue.select_set(self.selected_index)
            self.current_song = self.queue.get(self.selected_index)
            self.track_name.set(self.current_song)
            pygame.mixer.music.load(self.song_files[self.selected_index])
            pygame.mixer.music.play()
            self.queue.selection_clear(0, END)
    
    def check_music_end(self):
        if not pygame.mixer.music.get_busy() and not self.is_paused and self.song_files:
            self.skip_song()
        self.root.after(100, self.check_music_end)

root = Tk()
app = MusicPlayer(root)
root.mainloop()
