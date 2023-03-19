import openai

# TODO: Change this to a function reading api key from config file
openai.api_key = "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"

from pydub import AudioSegment


def speech_to_text(audio, section_num: int, output_file) -> None:
    total_length = len(song)
    print(f"debug: total length {total_length}, section number {section_num}")

    # FIXME: Probably have bug because of integer division
    section_length = total_length / section_num

    all_transcript = []
    for i in range(section_num):
        print(f"i = {i}", i*section_length, (i+1)*section_length)
        section = song[i*section_length: (i+1)*section_length]

        filename = f"data/abc_{i}.wav"
        section.export(filename, format="wav")

        # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
        audio_file= open(filename, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        # print(transcript["text"])
        # all_transcript.append(transcript["text"])
        print(transcript["text"], file=f)


song = AudioSegment.from_file(file="./data/abc.mov", format="mov")

# PyDub handles time in milliseconds
ten_seconds = 10 * 1000

section_num = 2

for section_num in range(1, 10):
    with open(f"data/{section_num}_sections", "w+") as f:
        speech_to_text(audio=song, section_num=section_num, output_file=f)
