from __future__ import annotations

import asyncio
import logging
from pathlib import Path
import asyncio
import aiofiles
import os
from pathlib import Path
from typing import Optional

import openai
import constants


# TODO: Change this to a function reading api key from config file
openai.api_key = "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"


async def _transcribe(audio_file: Path, prompt: str = "") -> str:
    """Function that actual calls openai API to do transcribe."""
    with open(audio_file, "rb") as f:
        logging.info(f"Start recognizing {audio_file}")
        t = await openai.Audio.atranscribe(
            model="whisper-1", 
            file=f, 
            prompt=prompt,
            language="ja"
        )
        text = t['text']
        logging.info(f"Finish recognizing {audio_file}")
        logging.debug(f"Recognized text: {text}")
        return text



async def watch_directory(directory: Path) -> Path:
    while True:
        # FIXME: This is not efficient, but it works for now
        files = sorted(list(directory.glob("*.wav")), key=lambda f: f.stat().st_mtime)
        if files:
            logging.debug(f"Found new audio file: {files[0]}, len({files}) unprocessed audio files")
            return files[0]
        else:
            await asyncio.sleep(1)


async def transcribe_audio(
    input_dir: Path = constants.NEW_AUDIO_PATH, done_audio_dir: Path = constants.DONE_AUDIO_PATH, text_file: Optional[Path] = None
) -> None:
    """Transcribes audio files in input_dir and appends results to text_file."""

    input_dir.mkdir(parents=True, exist_ok=True)
    done_audio_dir.mkdir(parents=True, exist_ok=True)

    if text_file is None:
        text_file = constants.CACHE_PATH / "transcriptions.txt"

    prompt = "始めます、写し込んでください。",  # Instruct to generate punctuated text
    while True:
        audio_file = await watch_directory(input_dir)
        text = await _transcribe(audio_file, prompt=prompt)
        if text == prompt:
            continue
        prompt = text

        async with aiofiles.open(text_file, "a") as f:
            await f.write(f"{text}\n")

        logging.info(f"Wrote text to {text_file}")

        # Move the processed audio file to the done_audio directory
        done_audio_file = done_audio_dir / audio_file.name
        os.rename(audio_file, done_audio_file)
        logging.debug(f"Moved {audio_file} to {done_audio_file}")
