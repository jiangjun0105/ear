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

# Constants
SAMPLE_RATE = 44100
NUM_CHANNELS = 1
BUFFER_SIZE = 1024


# Callback function to process audio
def callback(audio_queue: queue.Queue) -> Callable:
    def _callback(in_data: bytes, frame_count: int, time_info: dict, status: int) -> tuple:
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        audio_queue.put(audio_data)
        return (in_data, pyaudio.paContinue)

    return _callback

# Function to save audio data to WAV files
def save_audio(audio_queue: queue.Queue, recording_length: int) -> None:
    while True:
        audio_data = np.array([], dtype=np.int16)
        start_time = time.strftime("%Y%m%d-%H%M%S", time.gmtime())

        # Collect recording_length seconds of audio data
        print(f"Debug: {type(audio_queue)}, {type(recording_length)}")
        for _ in range(int(SAMPLE_RATE / BUFFER_SIZE * recording_length)):
            audio_data = np.concatenate((audio_data, audio_queue.get()))

        # Convert raw audio data to an AudioSegment
        audio_segment = AudioSegment(
            audio_data.tobytes(), sample_width=2, frame_rate=SAMPLE_RATE, channels=NUM_CHANNELS
        )

        # Save the audio segment as a WAV file
        output_filename = constants.CACHE_PATH / "new_audio" / f"{start_time}.wav"
        output_filename.parent.mkdir(parents=True, exist_ok=True)
        audio_segment.export(output_filename, format="wav")
        # Put the output_filename in the output_queue
        # run_coroutine_threadsafe(file_queue.put(output_filename), asyncio.get_event_loop())
        # await file_queue.put(output_filename)
        logging.info("Finished collecting audio")


async def collect_audio(recording_length: int = 30) -> None:
    audio_queue = queue.Queue()

    # Set up pyaudio stream
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
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

