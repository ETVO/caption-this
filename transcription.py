import os
import tempfile
import ffmpeg
import whisper
from time import time
from math import floor
from utils import format_timestamp
from typing import Iterator

model = None
MODEL_NAME = "large-v3"


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


def transcribe_audio(audio_filepath):
    time_start = time()
    if not model:
        load_whisper()

    print("Transcribing extracted audio...")
    result = model.transcribe(audio_filepath, fp16=False)
    time_elapsed = time() - time_start
    print(f"Transcription took {floor(time_elapsed)}s. Finished transcribing.")
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
