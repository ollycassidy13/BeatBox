import pygame
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import time

pygame.mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("BeatBox")
        self.root.minsize(800, 580)
        self.root.configure(bg='#ffffff')
        
        style = ttk.Style()
        style.configure('TButton', background='#d3d3d3', foreground='#333333', font=('Helvetica', 12))
        style.map('TButton', background=[('active', '#b0b0b0')])
        style.configure('TLabel', background='#ffffff', foreground='#333333', font=('Helvetica', 12))
        style.configure('TListbox', background='#f0f0f0', foreground='#333333', font=('Helvetica', 12))
        style.configure('TProgressbar', troughcolor='#ffffff', background='#333333')

        # Track frame
        self.track_frame = Frame(self.root, bg="#ffffff")
        self.track_frame.place(relx=0.0125, rely=0.025, relwidth=0.975, relheight=0.25)
        
        # Track frame label
        self.track_label = ttk.Label(self.root, text="Current Track", font=("Helvetica", 12, "bold"), background="#ffffff", foreground="#333333")
        self.track_label.place(relx=0.0225, rely=0.008)
        
        # Track name
        self.track_name_var = StringVar()
        self.track_name = ttk.Label(self.track_frame, textvariable=self.track_name_var, font=("Helvetica", 16), background="#ffffff")
        self.track_name.place(relx=0.225, rely=0.1)

        # Album cover
        self.album_cover_label = Label(self.track_frame, bg='#ffffff')
        self.album_cover_label.place(relx=0.0125, rely=0.2, relwidth=0.1875, relheight=0.8)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.track_frame, orient=HORIZONTAL, length=100, mode='determinate')
        self.progress.place(relx=0.225, rely=0.6, relwidth=0.75, relheight=0.2)

        # Time labels
        self.elapsed_time_label = ttk.Label(self.track_frame, text="0:00", font=("Helvetica", 10), background="#ffffff", foreground="#333333")
        self.elapsed_time_label.place(relx=0.225, rely=0.8)

        self.remaining_time_label = ttk.Label(self.track_frame, text="0:00", font=("Helvetica", 10), background="#ffffff", foreground="#333333")
        self.remaining_time_label.place(relx=0.975, rely=0.8, anchor='ne')

        # Control frame
        self.control_frame = Frame(self.root, bg="#ffffff")
        self.control_frame.place(relx=0.0125, rely=0.33, relwidth=0.975, relheight=0.1)
        
        # Control frame label
        self.control_label = ttk.Label(self.root, text="Control Panel", font=("Helvetica", 12, "bold"), background="#ffffff", foreground="#333333")
        self.control_label.place(relx=0.025, rely=0.30)
        
        # Control buttons
        self.load_button = ttk.Button(self.control_frame, text="Load Folder", command=self.load_folder)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.play_button = ttk.Button(self.control_frame, text="▶", command=self.play_song)
        self.play_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.pause_button = ttk.Button(self.control_frame, text="||", command=self.pause_song)
        self.pause_button.grid(row=0, column=2, padx=10, pady=10)
        
        self.stop_button = ttk.Button(self.control_frame, text="■", command=self.stop_song)
        self.stop_button.grid(row=0, column=3, padx=10, pady=10)

        self.skip_button = ttk.Button(self.control_frame, text=">|", command=self.skip_song)
        self.skip_button.grid(row=0, column=4, padx=10, pady=10)

        self.remove_button = ttk.Button(self.control_frame, text="Remove Song", command=self.remove_songs)
        self.remove_button.grid(row=0, column=5, padx=10, pady=10)
        
        # Listbox frame
        self.listbox_frame = Frame(self.root, bg="#ffffff")
        self.listbox_frame.place(relx=0.0125, rely=0.49, relwidth=0.975, relheight=0.48)
        
        # Listbox frame label
        self.queue_label = ttk.Label(self.root, text="Queue", font=("Helvetica", 12, "bold"), background="#ffffff", foreground="#333333")
        self.queue_label.place(relx=0.025, rely=0.45)
        
        # Listbox for songs loaded
        self.queue = Listbox(self.listbox_frame, selectbackground="gold", selectmode=SINGLE, font=("Helvetica", 12), bg="#f0f0f0", fg="#333333")
        self.queue.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.listbox_frame, orient=VERTICAL, command=self.queue.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.queue.config(yscrollcommand=self.scrollbar.set)

        self.song_files = []
        self.folder_names = []
        self.song_to_cover = {}
        self.current_song = None
        self.is_paused = False
        self.stopped = False
        self.selected_index = 0

        # Check for end of track event
        self.check_music_end()

    def load_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            album_cover = None
            folder_name = os.path.basename(folder_path)
            self.track_name_var.set(folder_name)  # Set track name to folder name
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    album_cover = file_path
                elif file.endswith(".mp3"):
                    self.song_files.append(file_path)
                    self.folder_names.append(folder_name)
                    self.queue.insert(END, folder_name)
                    self.song_to_cover[file_path] = album_cover
                    if album_cover:
                        self.display_album_cover(album_cover)

    def display_album_cover(self, image_path):
        img = Image.open(image_path)
        img = img.resize((150, 150), Image.LANCZOS)
        self.album_cover = ImageTk.PhotoImage(img)
        self.album_cover_label.config(image=self.album_cover)
        self.album_cover_label.config(width=150, height=150)

    def remove_songs(self):
        selected_indices = self.queue.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            song_file = self.song_files[selected_index]
            self.queue.delete(selected_index)
            del self.song_files[selected_index]
            del self.folder_names[selected_index]
            if song_file in self.song_to_cover:
                del self.song_to_cover[song_file]
        
    def play_song(self):
        if self.stopped:
            self.stopped = False
            if self.queue.curselection():
                self.selected_index = self.queue.curselection()[0]
            else:
                self.queue.select_set(self.selected_index)
            self.current_song = self.queue.get(self.selected_index)
            self.track_name_var.set(self.folder_names[self.selected_index])
            song_file = self.song_files[self.selected_index]
            pygame.mixer.music.load(song_file)
            pygame.mixer.music.play()
            if song_file in self.song_to_cover:
                self.display_album_cover(self.song_to_cover[song_file])
            self.update_progress_bar()
        elif self.is_paused and not self.stopped:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.update_progress()
        else:
            if self.queue.curselection():
                self.selected_index = self.queue.curselection()[0]
            else:
                self.selected_index = 0
                self.queue.select_set(self.selected_index)
            
            if self.selected_index < len(self.song_files):
                self.current_song = self.queue.get(self.selected_index)
                self.track_name_var.set(self.folder_names[self.selected_index])
                song_file = self.song_files[self.selected_index]
                pygame.mixer.music.load(song_file)
                pygame.mixer.music.play()
                self.is_paused = False
                if song_file in self.song_to_cover:
                    self.display_album_cover(self.song_to_cover[song_file])
                self.update_progress_bar()

        self.queue.selection_clear(0, END)
        
    def pause_song(self):
        pygame.mixer.music.pause()
        self.is_paused = True
        
    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_paused = False
        self.stopped = True
        self.progress["value"] = 0
        self.elapsed_time_label.config(text="0:00")
        self.remaining_time_label.config(text=f"-{self.format_time(self.progress['maximum'])}")

    def skip_song(self):
        if self.selected_index + 1 < len(self.song_files):
            self.selected_index += 1
            self.queue.select_set(self.selected_index)
            self.current_song = self.queue.get(self.selected_index)
            self.track_name_var.set(self.folder_names[self.selected_index])
            song_file = self.song_files[self.selected_index]
            pygame.mixer.music.load(song_file)
            pygame.mixer.music.play()
            self.queue.selection_clear(0, END)
            if song_file in self.song_to_cover:
                self.display_album_cover(self.song_to_cover[song_file])
            self.update_progress_bar()
        else:
            self.selected_index = 0
            self.queue.select_set(self.selected_index)
            self.current_song = self.queue.get(self.selected_index)
            self.track_name_var.set(self.folder_names[self.selected_index])
            song_file = self.song_files[self.selected_index]
            pygame.mixer.music.load(song_file)
            pygame.mixer.music.play()
            self.queue.selection_clear(0, END)
            if song_file in self.song_to_cover:
                self.display_album_cover(self.song_to_cover[song_file])
            self.update_progress_bar()
    
    def update_progress_bar(self):
        song_length = pygame.mixer.Sound(self.song_files[self.selected_index]).get_length()
        self.progress["maximum"] = song_length
        self.update_progress()

    def update_progress(self):
        if pygame.mixer.music.get_busy() and not self.stopped:
            current_time = pygame.mixer.music.get_pos() / 1000
            song_length = self.progress["maximum"]
            self.progress["value"] = current_time
            self.elapsed_time_label.config(text=self.format_time(current_time))
            self.remaining_time_label.config(text=f"-{self.format_time(song_length - current_time)}")
            self.root.after(1000, self.update_progress)
    
    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02}"

    def check_music_end(self):
        if not pygame.mixer.music.get_busy() and not self.is_paused and self.song_files and not self.stopped:
            self.skip_song()
        self.root.after(100, self.check_music_end)

root = Tk()
app = MusicPlayer(root)
root.mainloop()
