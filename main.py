### Developed by ETVO ### 

import os
import pyfiglet
from concurrent.futures import ThreadPoolExecutor
from utils import filename, write_srt
from transcription import extract_audio_file, transcribe_audio

# Clear screen and present title
os.system('cls' if os.name == 'nt' else 'clear')
print(pyfiglet.figlet_format("Caption-This!", font="big"))

# Get video file path
while True:
    video_filepath = input("\nWhat video would you like to transcribe?\n\nPlease enter the path to the video file: ")

    video_name = filename(video_filepath)

    if os.path.exists(video_filepath):
        break
    else:
        print("\n\n-- The path was not found! --\n\nPlease try again...\n")

# Set SRT file output directory
srt_output_dir = input("\n\nTo which directory would you like to output the SRT file?\n(press Enter for default 'caption-this/'): ")
if srt_output_dir == "":
    srt_output_dir = "caption-this/"

# Extract audio from video
audio_filepath = extract_audio_file(video_filepath, video_name)

# Transcribe audio
with ThreadPoolExecutor(max_workers=1) as executor:
    # Submit concurrent thread
    future = executor.submit(transcribe_audio, audio_filepath) 
    print(pyfiglet.figlet_format("please wait...", font="slant"))
    # Get result 
    result = future.result()

# Create directory if inexistent, join SRT file path
os.makedirs(srt_output_dir, exist_ok=True)
srt_path = os.path.join(srt_output_dir, f"{video_name}.srt")
# Open file and write SRT
with open(srt_path, "w", encoding="utf-8") as srt:
    write_srt(result["segments"], file=srt)
