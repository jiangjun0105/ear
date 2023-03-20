"""Module to collect audio for transcribing."""

from __future__ import annotations

import asyncio
import logging
from typing import Any
from pathlib import Path


async def collect_audio(queue: asyncio.Queue) -> None:
    """Interface of audio collecting module."""
    filename = Path("./data/abc.wav")
    while True:
        logging.info("Start collecting audio")
        # FIXME: Simulate collecting 30s long audio from microphone
        audio_file = filename
        await asyncio.sleep(3)
        await queue.put(audio_file)
        logging.info("Finished collecting audio")

