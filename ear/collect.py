"""Module to collect audio for transcribing."""

from __future__ import annotations

import asyncio
import logging
import asyncio
import pyaudio
import numpy as np
from pydub import AudioSegment
import threading
import queue
import time
from typing import Callable
import constants
import webrtcvad

# Constants
SAMPLE_RATE = 16000
NUM_CHANNELS = 1
FORMAT = pyaudio.paInt16
FRAME_DURATION_MS = 30
BUFFER_SIZE = SAMPLE_RATE * FRAME_DURATION_MS // 1000
NOISE_THRESHOLD = 15

# Callback function to process audio
def callback(audio_queue: queue.Queue) -> Callable:
    def _callback(in_data: bytes, frame_count: int, time_info: dict, status: int) -> tuple:
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        audio_queue.put(audio_data)
        return (in_data, pyaudio.paContinue)

    return _callback

# Function to save audio data to WAV files
def save_audio(audio_queue: queue.Queue, recording_length: int, detect_voice=True) -> None:
    # Number of frames to collect for this audio file
    num_frames = int(SAMPLE_RATE / BUFFER_SIZE * recording_length)
    if detect_voice:
        # Set VAD aggressiveness (0-3, 3 is most aggressive)
        vad = webrtcvad.Vad(3)  
        has_voice = 0

    while True:
        frames = []
        start_time = time.strftime("%Y%m%d-%H%M%S", time.gmtime())

        # Collect recording_length seconds of audio data
        print(f"Debug: {type(audio_queue)}, {type(recording_length)}")
        for _ in range(num_frames):
            one_frame = audio_queue.get().tobytes()
            frames.append(one_frame)

            if detect_voice and vad.is_speech(one_frame, SAMPLE_RATE):
                has_voice += 1

        if detect_voice and has_voice < NOISE_THRESHOLD:
            logging.info("No voice detected, skipping")
            continue

        # Convert raw audio data to an AudioSegment
        audio_segment = AudioSegment(
            b''.join(frames), sample_width=2, frame_rate=SAMPLE_RATE, channels=NUM_CHANNELS
        )

        # Save the audio segment as a WAV file
        output_filename = constants.CACHE_PATH / "new_audio" / f"{start_time}.wav"
        output_filename.parent.mkdir(parents=True, exist_ok=True)
        audio_segment.export(output_filename, format="wav")
        logging.info("Finished collecting audio")


async def collect_audio(recording_length: int = 30) -> None:
    audio_queue = queue.Queue()

    # Set up pyaudio stream
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=NUM_CHANNELS,
                        rate=SAMPLE_RATE,
                        input=True,
                        output=False,
                        frames_per_buffer=BUFFER_SIZE,
                        stream_callback=callback(audio_queue))

    # Start the stream
    stream.start_stream()

    # Start a separate thread to save the audio data
    saving_thread = threading.Thread(target=save_audio, args=(audio_queue, recording_length))
    saving_thread.start()

    # Run the stream indefinitely
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        # Stop the stream and close the resources
        stream.stop_stream()
        stream.close()
        audio.terminate()

