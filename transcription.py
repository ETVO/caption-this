### Developed by ETVO ### 

import os
import tempfile
import ffmpeg
import whisper # https://pypi.org/project/openai-whisper/s
from time import time
from math import floor
from utils import format_timestamp
from typing import Iterator

model = None
MODEL_NAME = "large-v3" # best for multi-lingual tasks

def load_whisper():
    global model
    print(f'Loading OpenAI\'s Whisper, model "{MODEL_NAME}"...')
    model = whisper.load_model(MODEL_NAME)


def extract_audio_file(video_filepath, video_name):
    print(f"Extracting audio from {video_name}...")
    # Get temporary directory to store audio file
    temp_dir = tempfile.gettempdir()

    audio_output_path = os.path.join(temp_dir, f"{video_name}.wav")

    # Extract audio and store in temp_dir
    ffmpeg.input(video_filepath).output(
        audio_output_path, acodec="pcm_s32le", ac=1, ar="16k"
    ).run(overwrite_output=True)

    print("Finished extracting.")
    return audio_output_path


def transcribe_audio(audio_filepath, task='transcribe'):
    time_start = time() # Start counting
    if not model:
        load_whisper()    

    # Get printable name for task 
    task_desc = 'Transcribing' if task == 'transcribe' else 'Translating' 
    print(f"{task_desc} extracted audio...")
    
    # Call model transcribe
    result = model.transcribe(audio_filepath, fp16=False, task=task)
    
    time_elapsed = time() - time_start
    print(f"Finished {task_desc.lower()} in {floor(time_elapsed)}s.")
    return result


def return_srt(transcript: Iterator[dict]):
    print("Generating SRT...")

    srt = ""

    for i, segment in enumerate(transcript, start=1):
        srt += f"""{i}\n
        {format_timestamp(segment['start'], always_include_hours=True)} --> 
        {format_timestamp(segment['end'], always_include_hours=True)}\n
        {segment['text'].strip().replace('-->', '->')}\n"""

    print("Finished generating.")
    return srt
