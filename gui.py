from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import time
from math import floor
from tkinter import *
from tkinter.messagebox import askyesno
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from utils import filename
from transcription import extract_audio_file, transcribe_audio, return_srt

video_filepath = ""
video_name = ""
saved = True


def select_video_file():
    """Select video file"""
    global video_filepath, video_name

    # Confirm dialog if unsaved
    if not saved:
        if not askyesno(
            title="Unsaved progress",
            message="If you select a new video file,"
            + "your unsaved progress will be lost."
            + "\nAre you sure you wish to continue?",
        ):
            return

    filepath = askopenfilename()

    if not filepath:
        return

    video_filepath = filepath
    video_name = filename(filepath)

    # Set title
    root.title(f"{BASE_TITLE}  - {video_name}")

    # Start transcription in separate thread
    Thread(target=start_transcription).start()


def save_file_as():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension=".srt",
        filetypes=[
            ("SubRip .srt", "*.srt"),
            ("Text Files", "*.txt"),
            ("All Files", "*.*"),
        ],
    )

    if not filepath:
        return

    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = text_input.get("1.0", END)
        output_file.write(text)

    # Set title and saved
    root.title(f"{BASE_TITLE}  - {video_name}")
    global saved
    saved = True


# Transcript coordinator function
def start_transcription():
    # Disable all buttons
    btn_open["state"] = "disabled"
    btn_save["state"] = "disabled"

    # Extract audio from selected video
    label["text"] = f"Extracting audio from {video_name}..."
    root.update()
    audio_filepath = None
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(extract_audio_file, video_filepath, video_name)
        audio_filepath = future.result()

    # Transcribe audio using whisper
    time_start = time()
    result = None
    with ThreadPoolExecutor(max_workers=1) as executor:
        label["text"] = f"Transcribing extracted audio. Please wait..."
        root.update()
        future = executor.submit(transcribe_audio, audio_filepath)
        result = future.result()

    # Get transcript in SRT format
    time_elapsed = time() - time_start
    srt_text = None
    with ThreadPoolExecutor(max_workers=1) as executor:
        label["text"] = f"Generating SRT..."
        root.update()
        future = executor.submit(return_srt, result["segments"])
        srt_text = future.result()

    # Show transcript in Text input
    label["text"] = f"Transcription took {floor(time_elapsed)}s. Transcription finished"

    text_input.delete("1.0", END)
    text_input.insert(END, srt_text)

    # Enable all buttons again
    btn_open["state"] = "disabled"
    btn_save["state"] = "disabled"

    # Show title and unsaved
    root.title(f"{BASE_TITLE}  - {video_name}*")
    global saved
    saved = False


root = Tk()
BASE_TITLE = "Caption-This!"
root.title(BASE_TITLE)

root.rowconfigure(0, minsize=600, weight=1)
root.columnconfigure(1, minsize=900, weight=1)

# Setup styles
s = Style().configure("EditFrame.TFrame", background="skyblue")

# Left column setup
left_frame = Frame(root, relief=RAISED, border=2)
btn_open = Button(left_frame, text="Select Video File", command=select_video_file)
btn_save = Button(left_frame, text="Save As...")

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)


# Right column setup
right_frame = Frame(root, style="EditFrame.TFrame")
label = Label(right_frame, text="Select a video file to start.")

text_frame = Frame(right_frame)
text_frame.columnconfigure(0, minsize=900, weight=1)
text_frame.rowconfigure(0, minsize=600, weight=1)
text_input = Text(text_frame)
scroller = Scrollbar(text_frame, command=text_input.yview)
text_input["yscrollcommand"] = scroller.set

# Left column layout
left_frame.grid(row=0, column=0, sticky="ns")

# Right column layout
right_frame.grid(row=0, column=1, sticky="nsew")

label.pack(fill="x")
text_frame.pack(fill="both")

text_input.grid(row=0, column=0, sticky="nsew")
scroller.grid(row=0, column=1, sticky="nsew")

root.mainloop()
