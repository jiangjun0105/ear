from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from pydub import AudioSegment
import openai


# TODO: Change this to a function reading api key from config file
openai.api_key = "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"

_CACHE_PATH = Path.home() / ".ear"

async def _transcribe(audio_file: Path) -> str:
    """Function that actual calls openai API to do transcribe."""
    with open(audio_file, "rb") as f:
        logging.info(f"Start recognizing {audio_file}")
        t = await openai.Audio.atranscribe(
            model="whisper-1", 
            file=f, 
            prompt="始めます、写し込んでください。",  # Instruct to generate punctuated text
            language="ja"
        )
        logging.info(f"Finish recognizing {audio_file}")
        return t


async def transcribe_audio(queue: asyncio.Queue, text_file: Path = _CACHE_PATH / "text") -> None:
    """Transcribes audio files in queue and appends results to text_file."""
    text_file.parent.mkdir(parents=True, exist_ok=True)
    while True:
        audio_file = await queue.get()
        t = await _transcribe(audio_file)
        with open(text_file, "a") as f:
            print(t["text"], file=f)
        logging.info(f"Wrote text to {text_file}")
        queue.task_done()