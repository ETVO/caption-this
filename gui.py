### Developed by ETVO ###

from concurrent.futures import (
    ThreadPoolExecutor,
)  # Used to prevent window not responding
from threading import Thread
from time import time
from math import floor
from tkinter import *
from tkinter.messagebox import askyesno
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from utils import filename, dirname, get_ico_file
from transcription import extract_audio_file, transcribe_audio, return_srt

video_filepath = ""
video_name = ""
saved = True
srt_texts = {}  # Store different versions of SRT text (Original and Translated)


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
    root.title(f"{BASE_TITLE} - {video_name}")
    video_label["text"] = "Video selected.\nClick Start to begin."
    # Enable Start and Task Options
    btn_start["state"] = "enabled"
    task_option["state"] = "enabled"


def start_button_click():
    """Start processing selected video"""
    if not video_filepath:
        return

    # Confirm dialog if unsaved
    if not saved:
        if not askyesno(
            title="Unsaved progress",
            message="If you select a new video file,"
            + "your unsaved progress will be lost."
            + "\nAre you sure you wish to continue?",
        ):
            return

    btn_start["state"] = "disabled"

    # Start transcription in separate thread
    Thread(target=start_transcription).start()


def save_as_file():
    """Save text(s) as file(s)."""
    if not srt_texts:
        return  # No texts to save

    flag_return = False

    initialdir = dirname(video_filepath)

    for key, text in srt_texts.items():
        initialfile = (
            f"{video_name}_{'Original' if key == 'transcribe' else 'Translated'}.srt"
        )
        filepath = asksaveasfilename(
            defaultextension=".srt",
            filetypes=[
                ("SubRip Subtitles (SRT)", "*.srt"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*"),
            ],
            initialfile=initialfile,
            initialdir=initialdir,
        )

        if not filepath:
            continue
        flag_return = True

        # Update initialdir if to chosen filepath
        initialdir = dirname(filepath)

        with open(filepath, mode="w", encoding="utf-8") as output_file:
            output_file.write(text)

    if not flag_return:
        return  # No filepaths were set

    # Set title and saved
    root.title(f"{BASE_TITLE} - {video_name}")
    global saved
    saved = True


def enable_buttons(enabled=True):
    """Enable or disable all buttons"""

    btn_open["state"] = "enabled" if enabled else "disabled"
    btn_save["state"] = "enabled" if enabled else "disabled"
    btn_start["state"] = "enabled" if enabled else "disabled"
    task_option["state"] = "enabled" if enabled else "disabled"
    update_version_radios(enabled)


def update_version_radios(enabled):
    """Update the state of version choice radio buttons"""

    if not enabled:
        version_radios["Original"]["state"] = "disabled"
        version_radios["Translated"]["state"] = "disabled"
        return

    match selected_task.get():
        case "Transcribe":
            version_radios["Original"]["state"] = "enabled"
            version_radios["Translated"]["state"] = "disabled"
            selected_version.set("Original")
        case "Translate":
            version_radios["Original"]["state"] = "disabled"
            version_radios["Translated"]["state"] = "enabled"
            selected_version.set("Translated")
        case "Both":
            version_radios["Original"]["state"] = "enabled"
            version_radios["Translated"]["state"] = "enabled"
            selected_version.set("Original")


def update_text_input():
    """Update displayed text according to version selected by user"""
    srt_text = ""
    if not srt_texts:
        return  # Early bird gets the worm

    match selected_version.get():
        case "Original":
            srt_text = srt_texts.get("transcribe")
        case "Translated":
            srt_text = srt_texts.get("translate")

    text_input.delete("1.0", END)
    text_input.insert(END, srt_text)


def on_change_text_input(*args):
    """Detect change in text input and update stored texts"""
    if not video_filepath:
        return  # Early bird

    new_srt_text = text_input.get("1.0", END)

    match selected_version.get():
        case "Original":
            srt_texts["transcribe"] = new_srt_text
        case "Translated":
            srt_texts["translate"] = new_srt_text


def start_transcription():
    """Orderly call the transcription functions"""
    # Disable all buttons while processing
    enable_buttons(False)

    # Extract audio from selected video
    info_label["text"] = f"Extracting audio from {video_name}..."
    root.update()
    audio_filepath = None
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(extract_audio_file, video_filepath, video_name)
        audio_filepath = future.result()

    # Transcribe and/or Translate audio using Whisper
    time_start = time()

    # Get tasks to perform
    tasks = []
    match selected_task.get():
        case "Transcribe":
            tasks = ["transcribe"]
        case "Translate":
            tasks = ["translate"]
        case "Both":
            tasks = ["transcribe", "translate"]

    global srt_texts
    helper_text = {"transcribe": "Transcribing", "translate": "Translating"}

    # Transcribe and/or Translate audio using Whisper
    for task in tasks:
        result = None
        with ThreadPoolExecutor(max_workers=1) as executor:
            info_label["text"] = f"{helper_text[task]} extracted audio. Please wait..."
            root.update()
            future = executor.submit(transcribe_audio, audio_filepath, task)
            result = future.result()

        # Get transcript in SRT format
        srt_text = None
        with ThreadPoolExecutor(max_workers=1) as executor:
            info_label["text"] = f"Generating SRT..."
            root.update()
            future = executor.submit(return_srt, result["segments"])
            srt_text = future.result()

        srt_texts[task] = srt_text  # Save to dict associated with task name

    # Show transcript in Text input
    time_elapsed = time() - time_start
    info_label["text"] = f"Transcription finished in {floor(time_elapsed)}s."

    # Enable all buttons again
    enable_buttons()
    update_text_input()  # Update text input to show SRT text
    # Show title and unsaved
    root.title(f"{BASE_TITLE} - {video_name}*")
    global saved
    saved = False


root = Tk()
BASE_TITLE = "Caption-This!"
root.title(BASE_TITLE)
root.iconbitmap(default=get_ico_file())

root.rowconfigure(0, minsize=600, weight=1)
root.columnconfigure(1, minsize=800, weight=1)

# Left column setup
left_frame = Frame(root, relief=RAISED, border=2)
btn_open = Button(left_frame, text="Select Video File", command=select_video_file)
video_label = Label(left_frame, text="")

selected_task = StringVar(left_frame, value="Transcribe")
task_option = OptionMenu(
    left_frame, selected_task, selected_task.get(), *["Transcribe", "Translate", "Both"]
)
task_option.configure(state="disabled")

btn_start = Button(
    left_frame, text="Start", state="disabled", command=start_button_click
)
btn_save = Button(left_frame, text="Save As...", state="disabled", command=save_as_file)


# Right column setup
right_frame = Frame(root)
# Info frame
info_frame = Frame(right_frame)
# info_frame.columnconfigure([0,1], minsize=400, weight=1)
info_label = Label(info_frame, text="Select a video file to start.")

selected_version = StringVar(info_frame, value="Original")
version_values = ["Original", "Translated"]
# Store radio buttons in dict so we can access them later
version_radios = dict()
for opt in version_values:
    version_radios[opt] = Radiobutton(
        info_frame,
        text=opt,
        variable=selected_version,
        value=opt,
        state="disabled",
        command=update_text_input,
    )
    version_radios[opt].pack(side=LEFT)

# Text frame
text_frame = Frame(right_frame)
text_frame.columnconfigure(0, minsize=900, weight=1)
text_frame.rowconfigure(0, minsize=600, weight=1)
text_input = Text(
    text_frame,
)
text_input.bind("<KeyRelease>", on_change_text_input)
scroller = Scrollbar(text_frame, command=text_input.yview)
text_input["yscrollcommand"] = scroller.set

# Left column layout
left_frame.grid(row=0, column=0, sticky="ns")
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
video_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
task_option.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_start.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

# Right column layout
right_frame.grid(row=0, column=1, sticky="nsew")

info_frame.pack(fill="x")
info_label.pack()

text_frame.pack(fill="both")
text_input.grid(row=0, column=0, sticky="nsew")
scroller.grid(row=0, column=1, sticky="nsew")

root.mainloop()
