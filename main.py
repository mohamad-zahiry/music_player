#!/usr/bin/env python3

import threading
import time
import os

import tkinter as tk
from tkinter import filedialog as tk_filedialog

import player


"""
controls the duration-thread
If True: the duration-thread stops
"""
end_of_program = False


class CustomTk(tk.Tk):
    def destroy(self) -> None:
        """
        Using "end_of_program" global variable to controll if user trys to
        close the app, stoping the duration-thread
        """
        global end_of_program
        end_of_program = True
        return super().destroy()


# global audio player
player = player.Player()


root = CustomTk()
root.title("Music Player")


# ============= start: Add music to "Music List" =============
# supported music types
__music_types = [
    ("Audio formats", ".mp3"),
    ("Audio formats", ".mp4"),
    ("Audio formats", ".wav"),
    ("Audio formats", ".flac"),
    ("Audio formats", ".aac"),
    ("Audio formats", ".ac3"),
    ("Audio formats", ".m4a"),
    ("Audio formats", ".aiff"),
    ("Audio formats", ".ogg"),
    ("Audio formats", ".adts"),
    ("Audio formats", ".opus"),
    ("Audio formats", ".ts"),
]

# opens a file dialog to select music files with support types
def get_music_dir():
    music_names = tk_filedialog.askopenfilenames(
        parent=root,
        initialdir=os.getcwd(),
        title="Please select one or more files:",
        filetypes=__music_types,
    )
    music_list.insert(0, *music_names)


add_path = tk.Button(root, text="Add Music", command=get_music_dir)
add_path.pack(side=tk.BOTTOM)
# ============= end: Add music to "Music List" =============


# ============= start: Music ListBox =============
bottom_frame = tk.Frame(root, pady=20)
bottom_frame.pack(side=tk.TOP)


def onselect(event):
    global player
    cur_select = music_list.get(music_list.curselection())
    player.stop()
    player.set_audio(cur_select)
    player.play()


music_list = tk.Listbox(bottom_frame, selectmode=tk.SINGLE)
music_list.config(width=32)
music_list.pack(side=tk.BOTTOM)

music_list.bind("<<ListboxSelect>>", onselect)
# ============= end: Music ListBox =============


# ========= start: topframe =========
setting_frame = tk.Frame(root)
setting_frame.pack(side=tk.TOP)
# ========= end: topframe =========


# ============= start: Volume =============
def set_volume(event):
    player.audio_set_volume(int(volume.get()))


volume = tk.Scale(setting_frame, from_=0, to=100, resolution=1, label="Volume", command=set_volume)
volume.pack(side=tk.LEFT)
# ============= end: Volume =============


# ============= start: Equalizer =============
def set_equalizer(event):
    player.set_equalizer(int(equalizer.get()))


equalizer = tk.Scale(setting_frame, from_=-20, to=20, resolution=1, label="Amplifier", command=set_equalizer)
equalizer.pack(side=tk.LEFT)
# ============= end: Equalizer =============


# ============= start: Rate scale =============
def set_rate(event):
    player.set_rate(int(rate.get()) / 100)


rate = tk.Scale(setting_frame, from_=30, to=300, resolution=1, label="speed", command=set_rate)
rate.pack(side=tk.LEFT)
# ============= end: Rate scale =============


# ============= start: control buttons =============
middle_frame = tk.Frame(root)
middle_frame.pack(side=tk.TOP, expand=True)

img_fast_backward = tk.PhotoImage(file="./icons/fast-backward.png")
fast_backward = tk.Label(middle_frame, image=img_fast_backward)
fast_backward.grid(column=0, row=0, padx=10)

img_previous_song = tk.PhotoImage(file="./icons/previous.png")
previous_song = tk.Label(middle_frame, image=img_previous_song)
previous_song.grid(column=1, row=0, padx=10)

img_pause_play = tk.PhotoImage(file="./icons/play.png")
pause_play = tk.Label(middle_frame, image=img_pause_play)
pause_play.grid(column=2, row=0, padx=10)

img_next_song = tk.PhotoImage(file="./icons/next.png")
next_song = tk.Label(middle_frame, image=img_next_song)
next_song.grid(column=3, row=0, padx=10)

img_fast_forward = tk.PhotoImage(file="./icons/fast-forward.png")
fast_forward = tk.Label(middle_frame, image=img_fast_forward)
fast_forward.grid(column=4, row=0, padx=10)
# ============= end: control buttons =============


# ============= start: Duration scale =============
"""
Prevents "set_duration" from moving the "duration" scale
when the mouse grabs the "duration" scale handle

If True: "set_duration" won't move the "duration" handle
"""
is_mouse_pressed = False


def mouse_pressed(event):
    """
    Turns the "is_mouse_pressed" to True to prevent moving
    "duration" scale by "set_duration"
    """
    global is_mouse_pressed
    is_mouse_pressed = True


def mouse_released(event):
    global is_mouse_pressed
    # Turns "is_mouse_pressed" to False to allow
    # "set_duration" moving the "duration" handle
    is_mouse_pressed = False
    pos_in_percent = int(duration.get())
    real_pos = pos_in_percent / 100
    player.set_position(real_pos)


duration = tk.Scale(
    middle_frame,
    from_=0,
    to=100,
    resolution=1,
    orient=tk.HORIZONTAL,
)

# bind "Left Click Pressed"
duration.bind("<ButtonPress-1>", mouse_pressed)
# bind "Left Click Released"
duration.bind("<ButtonRelease-1>", mouse_released)

duration.config(length=250)
duration.grid(column=0, row=1, columnspan=5)
# ============= end: Duration scale =============


# ============= Initialize primary values =============
def initialize():
    player.audio_set_volume(50)
    equalizer.set(0)
    volume.set(50)
    rate.set(100)


# ============= Updates duration scale =============
def set_duration(ended):
    global is_mouse_pressed, end_of_program, player
    while True:
        if ended():
            break
        if not is_mouse_pressed:
            pos_in_percent = player.get_position_percent()
            duration.set(pos_in_percent)
            # The "time.sleep" must used here. If doesn't,
            # the thread lock prevent program to stop
            time.sleep(0.01)


if __name__ == "__main__":
    initialize()

    # Used for breaks the "set_duration" function
    thread_handler = lambda: end_of_program

    set_duration_thread = threading.Thread(
        target=set_duration,
        args=(thread_handler,),
    )
    set_duration_thread.start()

    root.mainloop()
