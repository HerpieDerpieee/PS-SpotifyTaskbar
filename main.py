import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json

config = {}
with open("config.json", 'r') as file:
        config = json.load(file)

# Set up Spotipy OAuth with your Spotify API credentials
scope = config["scope"]
client_id = config['client_id']
client_secret = config["client_secret"]
redirect_uri = config["redirect_uri"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

SCREEN_WIDTH = 2560  
SCREEN_HEIGHT = 1440
WINDOW_HEIGHT = 40
WINDOW_WIDTH = 900

fetch_interval = 1000

class SpotifyWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Spotify Taskbar")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+0+{SCREEN_HEIGHT - WINDOW_HEIGHT}")
        self.overrideredirect(True) 
        self.wm_attributes("-topmost", True) 
        self.configure(background='#141414')

        # Make window transparent
        self.wm_attributes("-transparentcolor", "#141414")

        # Load and display Spotify logo
        self.logo_image = Image.open("spotify_logo.png")
        self.logo_image = self.logo_image.resize((30, 30))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self, image=self.logo_photo, bg="#141414")
        self.logo_label.pack(side="left", padx=5, pady=5)

        # Song info label
        self.song_label = tk.Label(self, text="Loading...", font=("Arial", 8), fg="white", bg="#141414")
        self.song_label.pack(side="top", anchor="w", padx=5, pady=0)

        # Custom style for the progress bar
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar",
                        thickness=5,
                        troughcolor='#457e59',
                        background='#1DB954',
                        troughrelief='flat',
                        bordercolor='#141414')

        # Playback bar
        self.playback_bar = ttk.Progressbar(self, orient="horizontal", length=WINDOW_WIDTH / 4, mode="determinate", style="TProgressbar")
        self.playback_bar.pack(side="top", anchor="w", padx=5, pady=0)

        # Update song info periodically
        self.update_song_info()

    def update_song_info(self):
        try:
            current_playback = sp.current_playback()
            if current_playback and "is_playing" in current_playback:
                if current_playback["is_playing"]:
                    track_name = current_playback["item"]["name"]
                    artist_name = current_playback["item"]["artists"][0]["name"]
                    current_time = current_playback["progress_ms"]
                    max_time = current_playback["item"]["duration_ms"]

                    self.song_label.config(text=f"{artist_name} - {track_name}")
                    self.playback_bar["value"] = (current_time / max_time) * 100
                else:
                    self.not_playing()
            else:
                self.not_playing()
        except Exception as e:
            print(e)
            self.not_playing()

        # Increase the delay to 5000 milliseconds (5 seconds)
        self.after(fetch_interval, self.update_song_info)

    def not_playing(self):
        self.song_label.config(text=f"Not Playing Anything :(")
        self.playback_bar["value"] = 0

if __name__ == "__main__":
    app = SpotifyWindow()
    app.mainloop()