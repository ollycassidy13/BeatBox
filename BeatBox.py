import pygame
import os
import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog, Listbox, LEFT, BOTH, Y, RIGHT, END
from PIL import Image, ImageTk
#import time

pygame.mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("BeatBox")
        self.root.minsize(1400, 620)
        ctk.set_appearance_mode("dark")

        # determine the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # path to the custom theme file
        custom_theme_path = os.path.join(script_dir, "theme1.json")
        # set the custom theme
        ctk.set_default_color_theme(custom_theme_path)

        # track frame
        self.track_frame = ctk.CTkFrame(self.root)
        self.track_frame.place(relx=0.0125, rely=0.03, relwidth=0.975, relheight=0.225)

        # track frame label
        self.track_label = ctk.CTkLabel(self.root, text="Current Track", font=("Helvetica", 12, "bold"))
        self.track_label.place(relx=0.02, rely=0.008)

        # track name
        self.track_name_var = ctk.StringVar()
        self.track_name = ctk.CTkLabel(self.track_frame, textvariable=self.track_name_var, font=("Helvetica", 16))
        self.track_name.place(relx=0.225, rely=0.1)

        # album cover
        self.album_cover_label = ctk.CTkLabel(self.track_frame, text="No Album Cover")
        self.album_cover_label.place(relx=0.0125, rely=0.2, relwidth=0.1875, relheight=0.8)

        # progress bar
        self.progress = ctk.CTkProgressBar(self.track_frame)
        self.progress.place(relx=0.225, rely=0.6, relwidth=0.75, relheight=0.2)

        # time labels
        self.elapsed_time_label = ctk.CTkLabel(self.track_frame, text="0:00", font=("Helvetica", 10))
        self.elapsed_time_label.place(relx=0.225, rely=0.8)

        self.remaining_time_label = ctk.CTkLabel(self.track_frame, text="0:00", font=("Helvetica", 10))
        self.remaining_time_label.place(relx=0.975, rely=0.8, anchor='ne')

        # control frame
        self.control_frame = ctk.CTkFrame(self.root)
        self.control_frame.place(relx=0.0125, rely=0.33, relwidth=0.82, relheight=0.1)

        # control frame label
        self.control_label = ctk.CTkLabel(self.root, text="Controls", font=("Helvetica", 12, "bold"))
        self.control_label.place(relx=0.025, rely=0.29)

        # control buttons
        self.load_button = ctk.CTkButton(self.control_frame, text="Load Folder", command=self.load_folder)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)

        self.prev_button = ctk.CTkButton(self.control_frame, text="|<", command=self.previous_song)
        self.prev_button.grid(row=0, column=1, padx=10, pady=10)

        self.play_button = ctk.CTkButton(self.control_frame, text="▶", command=self.play_song)
        self.play_button.grid(row=0, column=2, padx=10, pady=10)

        self.pause_button = ctk.CTkButton(self.control_frame, text="||", command=self.pause_song)
        self.pause_button.grid(row=0, column=3, padx=10, pady=10)

        self.stop_button = ctk.CTkButton(self.control_frame, text="■", command=self.stop_song)
        self.stop_button.grid(row=0, column=4, padx=10, pady=10)

        self.skip_button = ctk.CTkButton(self.control_frame, text=">|", command=self.skip_song)
        self.skip_button.grid(row=0, column=5, padx=10, pady=10)

        self.remove_button = ctk.CTkButton(self.control_frame, text="Remove Song", command=self.remove_songs)
        self.remove_button.grid(row=0, column=6, padx=10, pady=10)

        # spinning vinyl frame
        self.vinyl_frame = ctk.CTkFrame(self.root)
        self.vinyl_frame.place(relx=0.85, rely=0.33, relwidth=0.1, relheight=0.225)

        # vinyl image
        self.vinyl_image_path = os.path.join(script_dir, "vinyl2.jpg")
        self.vinyl_image = Image.open(self.vinyl_image_path)
        self.vinyl_image = self.vinyl_image.resize((120, 120), Image.LANCZOS)
        self.vinyl_image = ImageTk.PhotoImage(self.vinyl_image)
        self.vinyl_label = ctk.CTkLabel(self.vinyl_frame, image=self.vinyl_image)
        self.vinyl_label.image = self.vinyl_image
        self.vinyl_label.place(relx=0.5, rely=0.33, anchor='center')

        # listbox frame
        self.listbox_frame = ctk.CTkFrame(self.root)
        self.listbox_frame.place(relx=0.0125, rely=0.49, relwidth=0.975, relheight=0.48)

        # listbox frame label
        self.queue_label = ctk.CTkLabel(self.root, text="Queue", font=("Helvetica", 12, "bold"))
        self.queue_label.place(relx=0.025, rely=0.45)

        # listbox for songs loaded
        self.queue = Listbox(self.listbox_frame, font=("Helvetica", 12), bg="black", fg="gray", selectbackground="gray", selectforeground="black")
        self.queue.pack(side=LEFT, fill=BOTH, expand=True)

        # scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.listbox_frame, command=self.queue.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.queue.config(yscrollcommand=self.scrollbar.set)

        self.song_files = []
        self.folder_names = []
        self.song_to_cover = {}
        self.current_song = None
        self.is_paused = False
        self.stopped = False
        self.selected_index = 0

        # check for end of track event
        self.check_music_end()

        self.angle = 0
        self.update_progress()  # start updating
        
    def load_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            album_cover = None
            folder_name = os.path.basename(folder_path)
            self.track_name_var.set(folder_name)  # set track name to folder name
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
        self.album_cover = CTkImage(light_image=img, dark_image=img, size=(150, 150))
        self.album_cover_label.configure(image=self.album_cover, text="")
        
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
        # if stopped play current song from beginning
        if self.stopped:
            self.stopped = False
            # if a different song selected play that song from beginning
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
        # if paused play current song from paused place
        elif self.is_paused and not self.stopped:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.update_progress()
        else:
            if self.queue.curselection():
                self.selected_index = self.queue.curselection()[0]
            # play first song in queue
            else:
                self.selected_index = 0
                self.queue.select_set(self.selected_index)

            # play the music
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
        self.progress.set(0)
        self.elapsed_time_label.configure(text="0:00")
        self.remaining_time_label.configure(text=f"-{self.format_time(self.progress.get())}")

    def new_song(self):
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

    def skip_song(self):
        if self.selected_index + 1 < len(self.song_files):
            self.selected_index += 1
        else:
            self.selected_index = 0
        self.new_song()

    def previous_song(self):
        if (self.selected_index == 0):
            self.selected_index = len(self.song_files) - 1
        else:
            self.selected_index -= 1
        self.new_song()

    def update_progress_bar(self):
        song_length = pygame.mixer.Sound(self.song_files[self.selected_index]).get_length()
        self.progress.set(0)
        self.progress_length = song_length
        self.update_progress()  # start updating progress bar

    def update_progress(self):
        if pygame.mixer.music.get_busy() and not self.stopped:
            current_time = pygame.mixer.music.get_pos() / 1000
            self.progress.set(current_time / self.progress_length)
            self.elapsed_time_label.configure(text=self.format_time(current_time))
            self.remaining_time_label.configure(text=f"-{self.format_time(self.progress_length - current_time)}")
            if not self.stopped and self.song_files:
                self.angle += 5
                img = Image.open(self.vinyl_image_path)
                img = img.resize((150, 150), Image.LANCZOS)
                img = img.rotate(self.angle)
                self.vinyl_image = CTkImage(light_image=img, dark_image=img, size=(150, 150))
                self.vinyl_label.configure(image=self.vinyl_image)
                self.vinyl_label.image = self.vinyl_image
            self.root.after(1000, self.update_progress)  # keep updating progress 

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02}"

    def check_music_end(self):
        if not pygame.mixer.music.get_busy() and not self.is_paused and self.song_files and not self.stopped:
            self.skip_song()
        self.root.after(100, self.check_music_end)

root = ctk.CTk()
app = MusicPlayer(root)
root.mainloop()